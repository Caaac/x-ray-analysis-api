from typing import Annotated, Optional
from datetime import datetime
from sqlalchemy import ForeignKey, text, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base 
from .enum import XRayContext

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
xray_context = Annotated[Optional[XRayContext], mapped_column(SQLAlchemyEnum(XRayContext), nullable=True)]

class XRayRequestOrm(Base):
    __tablename__ = "mws_xray_request"

    id: Mapped[intpk]
    callback_url: Mapped[str]
    created_at: Mapped[created_at]

class XRayFileOrm(Base):
    __tablename__ = "mws_xray_file"

    id: Mapped[intpk]
    context_type: Mapped[xray_context]
    request_id: Mapped[int] = mapped_column(ForeignKey("mws_xray_request.id", ondelete="CASCADE"))
    file_id: Mapped[int] = mapped_column(ForeignKey("mws_file.id", ondelete="CASCADE"))

class FileOrm(Base):
    __tablename__ = "mws_file"

    id: Mapped[intpk]
    file_name: Mapped[str]
    file_size: Mapped[int]
    path: Mapped[str]
    content_type: Mapped[str]
    created_at: Mapped[created_at]

class XRayImagePredictedOrm(Base):
    __tablename__ = "mws_xray_predict"
    
    id: Mapped[intpk]
    xray_file_id: Mapped[int] = mapped_column(ForeignKey("mws_xray_file.id", ondelete="CASCADE"))
    predicted_at: Mapped[datetime | None]

class PredictedClassOrm(Base):
    __tablename__ = "mws_predicted_class"

    id: Mapped[intpk]
    xray_predict_id: Mapped[int] = mapped_column(ForeignKey("mws_xray_predict.id", ondelete="CASCADE"))
    class_id: Mapped[int] = mapped_column(ForeignKey("mws_classified.id", ondelete="CASCADE"))

class PredictedClassesOrm(Base):
    __tablename__ = 'mws_classified'

    id: Mapped[intpk]
    type_classification: Mapped[xray_context]
    class_id: Mapped[int]
    class_description: Mapped[str]

