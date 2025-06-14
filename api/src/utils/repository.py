from abc import ABC, abstractmethod
from src.db.database import async_session_factory
from sqlalchemy import select, insert

class AbstractRepository(ABC):
    @abstractmethod
    async def add():
        raise NotImplementedError
    
    @abstractmethod
    async def get():
        raise NotImplementedError
    

class SqlAlchemyRepository(AbstractRepository):
    model = None
    
    async def add(self, data: dict) -> int:
        async with async_session_factory() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            return (await session.execute(stmt)).scalar_one()

    async def get(self, id: int):
        async with async_session_factory() as session:
            stmt = select(self.model).where(self.model.id == id)
            return (await session.execute(stmt)).scalar_one()
    
    async def get_all(self):
        async with async_session_factory() as session:
            stmt = select(self.model)
            return (await session.execute(stmt)).scalars().all()
    
    

    