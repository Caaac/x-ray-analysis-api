from typing import Annotated
from datetime import datetime
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base 

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class XrayImageOrm(Base):
    __tablename__ = "mws_xray"

    id: Mapped[intpk]
    url_from: Mapped[str]
    image_path: Mapped[str]
    type: Mapped[str]
    created_at: Mapped[created_at]
    predicted_at: Mapped[datetime | None]


class XrayImagePredictedOrm(Base):
    __tablename__ = "mws_xray_predicted"

    id: Mapped[intpk]
    class_id: Mapped[int]
    image_id: Mapped[int] = mapped_column(ForeignKey("mws_xray.id", ondelete="CASCADE"))
    
