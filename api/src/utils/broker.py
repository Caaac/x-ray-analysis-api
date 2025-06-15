import aio_pika
from abc import ABC, abstractmethod


class AbstractBroker(ABC):

    @abstractmethod
    async def init_connection(self):
        raise NotImplementedError

    @abstractmethod
    async def close_connection(self):
        raise NotImplementedError

    # @abstractmethod
    # async def send_message(self, message):
    #     raise NotImplementedError


class RMQBroker(AbstractBroker):
    def __init__(
        self,
        connection_params: dict,
        queue_name: str,
        routing_key: str = None,
        exchange_name: str = None
    ):
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.connection_params = connection_params

        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None

    async def __aenter__(self):
        return await self.init_connection()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_connection()

    async def init_connection(self) -> AbstractBroker:
        self.connection: aio_pika.abc.AbstractRobustConnection = await aio_pika.connect_robust(**self.connection_params)

        self.channel: aio_pika.abc.AbstractChannel = await self.connection.channel()

        # TODO set exchange
        # self.exchange = await self.channel.declare_exchange(
        #   name=self.exchange_name,
        #   type=aio_pika.ExchangeType.DIRECT
        # )

        # await self.setup_queue({"durable": True})
        await self.setup_queue()
        await self.setup_connection_settings()

        return self

    async def setup_queue(self, **option) -> None:
        # self.queue: aio_pika.abc.AbstractQueue = await self.channel.declare_queue(self.queue_name, **option)
        self.queue: aio_pika.abc.AbstractQueue = await self.channel.declare_queue(self.queue_name, durable=True)

    async def setup_connection_settings(self) -> None:
        pass

    async def close_connection(self) -> None:
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def consume_messages(self, callback):
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                # async with message.process(): # Auto ack message
                await callback(message)
