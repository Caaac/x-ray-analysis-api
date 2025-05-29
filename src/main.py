import uvicorn
from fastapi import FastAPI
from src.api import api_router

app = FastAPI()
app.include_router(api_router)


def main():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
