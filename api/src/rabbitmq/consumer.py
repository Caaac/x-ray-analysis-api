import asyncio
import aio_pika

from src.utils.broker import RMQBroker
from src.config import settings


class RMQConsumer(RMQBroker):
    async def setup_connection_settings(self) -> None:
        await self.channel.set_qos(prefetch_count=1)


def debug(message):
    with open('test.txt', 'a') as f:
        f.write(message + '\n')


async def message_handler(message: aio_pika.abc.AbstractIncomingMessage):
    debug('message_handler')
    debug(f" [x] Received: {message.body.decode()}")
    await asyncio.sleep(10)
    await message.ack()

consumer_connection: RMQConsumer = None


async def start_conn():
    global consumer_connection
    consumer_connection = RMQConsumer(
        connection_params={
            "host": settings.MB_URL,
            "port": settings.MB_PORT,
            "login": settings.MB_USER,
            "password": settings.MB_PASSWORD
        },
        queue_name="xray_illnes_predict",
    )
    await consumer_connection.init_connection()
    await consumer_connection.consume_messages(message_handler)


async def close_conn():
    await consumer_connection.close_connection()
