from src.utils.repository import AbstractRepository
from src.schemas.broker import SXrayMessageResponse

class PredictResultService:
    def __init__(self, request_repository: AbstractRepository):
        self.request_repository: AbstractRepository = request_repository()
    
    async def get(self, predict_id: int):
        pass
    
    async def getList(self, request_id: int):
        pass
    
    async def setPredict(self, result: SXrayMessageResponse):
        return await self.request_repository.set_predicted_result(result)
