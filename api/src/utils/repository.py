from abc import ABC, abstractmethod
from api.src.db.database import async_session_factory

class AbstractRepository(ABC):
    
    @abstractmethod
    async def add():
        raise NotImplementedError
    
    @abstractmethod
    async def get():
        raise NotImplementedError
    

class SqlAlchemyRepository(AbstractRepository):
    model = None
    
    async def add(self, data: dict):
        pass

    async def get(self, id: int):
        pass
    