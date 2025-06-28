import os
import logging
import asyncio
import uvicorn
import traceback

from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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
    handlers=[
        logging.FileHandler(f'./logs/{datetime.now().strftime("%Y-%m-%d")}.log'),
        logging.StreamHandler()  # Добавляем вывод в консоль
    ],
    # filename=f'./logs/{datetime.now().strftime("%Y-%m-%d")}.log',
    # filemode='a'
)
logger = logging.getLogger(__name__)

async def custom_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    logger.error(f"Exception occurred: {str(exc)}\n{tb}")

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc),
            "detail": tb if settings.DEBUG else "Internal server error",
            "path": request.url.path
        }
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.add_exception_handler(Exception, custom_exception_handler)
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
                port=8000, reload=settings.DEBUG, log_config=None)


if __name__ == "__main__":
    main()
