import asyncio
from typing import Annotated

from sqlalchemy import String, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import settings

sync_engine = create_engine(
    url=settings.SYNC_DATABASE_URL,
    echo=settings.DEBUG,
)

async_engine = create_async_engine(
    url=settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
)

sync_session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
























async def get_test():
    # # async with async_engine.connect() as conn:
    # async with async_session_factory() as conn:
    #     # res = await conn.execute(text("SELECT VERSION()"))
    #     res = await conn.execute(text("SELECT * FROM mws_xray"))
    #     print(f"{res.one()}")
    with sync_engine.connect() as session:
        print(11)
        r = session.execute(text("SELECT VERSION()"))
        print(r.one())

async def main():
    
    await get_test()

if __name__ == "__main__":
	asyncio.run(main())

