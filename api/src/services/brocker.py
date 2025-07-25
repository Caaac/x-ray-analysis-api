import json
import aiohttp
import logging
import aio_pika

from src.utils.broker import RMQBroker
from src.utils.http_client import HttpClient
from src.schemas.broker import SXrayMessageResponse
from src.services.predict_result import PredictResultService
from src.repositories.xray_img_predict import XRayRequestRepository


class BrokerService:
    def __init__(self, conn: RMQBroker):
        self.conn: RMQBroker = conn

    async def send_message(self, message: str):
        async with self.conn as producer:
            await producer.send_message(message)

    @staticmethod
    async def xray_predict_handler(message: aio_pika.abc.AbstractIncomingMessage):

        obj = json.loads(message.body.decode())
        
        logging.info(f"Received message from RabbitMQ: {obj}")

        service = PredictResultService(XRayRequestRepository)
        predict_info = await service.setPredict(SXrayMessageResponse(**obj))

        callback_url = predict_info["callback_url"]
        del predict_info["callback_url"]

        http_clien = HttpClient({
            "Content-Type": "application/json; charset=utf-8",
            "Bitrix-Hms-Integration-Command": "set_xray_predict_result"
        })

        data = json.dumps(predict_info, ensure_ascii=False)

        try:
            responce = await http_clien.post(callback_url, data=data)
            logging.info(f"Success send predict to {callback_url}: {data}")
            logging.info(f"Response from {callback_url}: {responce}")
            await message.ack()
        except aiohttp.ClientResponseError as e:
            logging.error(
                f"HTTP error {e.status}: {e.message}\n"
                f"Message: {e.message}\n"
                f"Headers: {e.headers}"
            )
            raise
        except Exception as e:
            logging.exception(e)
            # TODO make DLX
            await message.nack(requeue=False)
            raise
