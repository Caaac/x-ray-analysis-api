from src.utils.broker import RMQBroker

class BrokerService:
    def __init__(self, conn: RMQBroker):
        self.conn: RMQBroker = conn

    async def send_message(self, message: str):
        async with self.conn as producer:
            await producer.send_message(message)