import logging

from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from src.utils.repository import SqlAlchemyRepository
from src.schemas.broker import SXrayMessageResponse
from src.db.database import async_session_factory
from src.db.models import (
    XRayFileOrm, 
    PredictedClassOrm, 
    XRayImagePredictedOrm, 
    PredictedClassifiedOrm as PCO
)


class XRayRequestRepository(SqlAlchemyRepository):
    model = XRayImagePredictedOrm

    async def set_predicted_result(self, result: SXrayMessageResponse) -> dict:
        async with async_session_factory() as session:
            try:
                query = (
                    select(XRayFileOrm)
                    .filter(XRayFileOrm.id == result.xray_file_id)
                    .options(
                        joinedload(XRayFileOrm.request),
                        joinedload(XRayFileOrm.file_data)
                    )
                )

                xray_img_info = (await session.execute(query)).scalar_one()

                stmt = select(PCO).filter(and_(
                    PCO.type_classification == xray_img_info.context_type,
                    PCO.class_id.in_(result.predicted_class)
                ))

                classifieds = (await session.execute(stmt)).scalars().all()

                new_predict = XRayImagePredictedOrm(
                    xray_file_id=xray_img_info.id,
                    predicted_at=datetime.now()
                )

                return_result = {
                    "request_id": xray_img_info.request.id,
                    "file_name": xray_img_info.file_data.file_name,
                    "callback_url": xray_img_info.request.callback_url,
                    "predicted_class": []
                }

                for classified in classifieds:
                    new_predict.classes.append(PredictedClassOrm(class_id=classified.id))
                    return_result["predicted_class"].append({
                        "class_id": classified.class_id,
                        "class_description": classified.class_description
                    })

                session.add(new_predict)
                await session.commit()
                return return_result

            except Exception as e:
                logging.exception(e)
                session.rollback()
