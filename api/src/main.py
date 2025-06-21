import os
import logging
import asyncio
import uvicorn

from fastapi import FastAPI
from datetime import datetime
from contextlib import asynccontextmanager

from src.api import api_router
from src.config import settings
from src.rabbitmq.consumer import start_conn, close_conn

# Logger
os.makedirs('./logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=f'./logs/{datetime.now().strftime("%Y-%m-%d")}.log',
    filemode='w' if settings.DEBUG else 'a'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = asyncio.create_task(start_conn())
    yield
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
    await close_conn()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.router.encoding = 'utf-8'


def main():
    uvicorn.run("src.main:app", host="0.0.0.0",
                port=8000, reload=True, log_config=None)


if __name__ == "__main__":
    main()
