import aio_pika
from src.utils.broker import RMQBroker
from src.config import settings


class RMQProducer(RMQBroker):
    async def send_message(self, message):
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=self.routing_key
        )


producer_connection: RMQProducer = RMQProducer(
    connection_params={
        "host": settings.MB_URL,
        "port": settings.MB_PORT,
        "login": settings.MB_USER,
        "password": settings.MB_PASSWORD
    },
    queue_name=settings.MB_PRODUCER_QUEUE,
    routing_key=settings.MB_PRODUCER_QUEUE,
)
