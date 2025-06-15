import asyncio
import uvicorn
from fastapi import FastAPI
from src.api import api_router
from contextlib import asynccontextmanager

from src.rabbitmq.consumer import start_conn, close_conn

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
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
