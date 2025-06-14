from src.utils.repository import SqlAlchemyRepository
from src.db.models import XRayRequestOrm
from src.db.database import async_session_factory
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class XRayRequestRepository(SqlAlchemyRepository):
    model = XRayRequestOrm
    
    async def get_with_files(self, id: int):
        async with async_session_factory() as session:
            query = (
                select(XRayRequestOrm)
                .options(selectinload(XRayRequestOrm.xray_files))
                .filter(XRayRequestOrm.id == id)
            )
            return (await session.execute(query)).scalar_one()