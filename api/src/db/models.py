from typing import Annotated, Optional
from datetime import datetime
from sqlalchemy import ForeignKey, text, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base 
from src.db.enums import XRayContext
from src.schemas.models import SXRayRequest, SXRayRequestRel, SFile

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
xray_context = Annotated[Optional[XRayContext], mapped_column(SQLAlchemyEnum(XRayContext), nullable=True)]

class XRayRequestOrm(Base):
    __tablename__ = "mws_xray_request"
    
    schema = SXRayRequest
    schema_rel = SXRayRequestRel

    id: Mapped[intpk]
    callback_url: Mapped[str]
    created_at: Mapped[created_at]
    
    xray_files: Mapped[list["XRayFileOrm"]] = relationship(
        back_populates="request"
    )

class XRayFileOrm(Base):
    __tablename__ = "mws_xray_file"

    id: Mapped[intpk]
    context_type: Mapped[xray_context]
    request_id: Mapped[int] = mapped_column(ForeignKey("mws_xray_request.id", ondelete="CASCADE"))
    file_id: Mapped[int] = mapped_column(ForeignKey("mws_file.id", ondelete="CASCADE"))
    
    request: Mapped["XRayRequestOrm"] = relationship(
        back_populates="xray_files"
    )
    
    file_data: Mapped["FileOrm"] = relationship()
    
    predict: Mapped["XRayImagePredictedOrm"] = relationship(
        back_populates="xray_file"
    )

class FileOrm(Base):
    __tablename__ = "mws_file"

    schema = SFile

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
    
    xray_file: Mapped["XRayFileOrm"] = relationship(
        back_populates="predict"
    )
    
    classes: Mapped[list["PredictedClassOrm"]] = relationship(
        back_populates="predict"
    )

class PredictedClassOrm(Base):
    __tablename__ = "mws_predicted_class"

    id: Mapped[intpk]
    xray_predict_id: Mapped[int] = mapped_column(ForeignKey("mws_xray_predict.id", ondelete="CASCADE"))
    class_id: Mapped[int] = mapped_column(ForeignKey("mws_classified.id", ondelete="CASCADE"))
    
    predict: Mapped["XRayImagePredictedOrm"] = relationship(
        back_populates="classes"
    )
    
    class_info: Mapped["PredictedClassifiedOrm"] = relationship()

class PredictedClassifiedOrm(Base):
    __tablename__ = 'mws_classified'

    id: Mapped[intpk]
    type_classification: Mapped[xray_context]
    class_id: Mapped[int]
    class_description: Mapped[str]
    
    
    
    

