import aiormq
import asyncio
import logging
import aio_pika


from src.utils.broker import RMQBroker
from src.config import settings


class RMQConsumer(RMQBroker):
    async def setup_connection_settings(self) -> None:
        await self.channel.set_qos(prefetch_count=1)


consumer_connection: RMQConsumer = None


async def start_conn():
    from src.services.brocker import BrokerService
   
    while True:
        consumer_connection = RMQConsumer(
            connection_params={
                "host": settings.MB_URL,
                "port": settings.MB_PORT,
                "login": settings.MB_USER,
                "password": settings.MB_PASSWORD
            },
            queue_name=settings.MB_CONSUMER_QUEUE,
        )

        try:
            await consumer_connection.init_connection()
            await consumer_connection.consume_messages(BrokerService.xray_predict_handler)
            logging.info("Consumer started successfully")
            return True
        except (aiormq.exceptions.AMQPConnectionError, ConnectionError) as ex:
            logging.error(
                f"Connection error: {ex}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as ex:
            logging.critical(f"Unexpected error: {ex}")
            logging.exception(f"Unexpected error: {ex}")
            return False


async def close_conn():
    if consumer_connection:
        await consumer_connection.close_connection()
