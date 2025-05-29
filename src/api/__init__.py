from fastapi import APIRouter
from src.api import xray

api_router = APIRouter()
api_router.include_router(xray.router)
