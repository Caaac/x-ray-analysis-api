from datetime import datetime
from pydantic import BaseModel, HttpUrl

from src.db.enums import XRayContext


class SFileAdd(BaseModel):
    file_name: str
    file_size: int
    path: str
    content_type: str
    created_at: datetime

class SFile(SFileAdd):
    id: int
    
class SPredictedClassesAdd(BaseModel):
    type_classification: XRayContext
    class_id: int
    class_description: str

class SPredictedClasses(SPredictedClassesAdd):
    id: int



class SXRayRequestAdd(BaseModel):
    callback_url: HttpUrl
    created_at: datetime | None = None
    
    # class Config:
    #     from_attributes = True

class SXRayRequest(SXRayRequestAdd):
    id: int
    
    
class SXRayFileAdd(BaseModel):
    context_type: XRayContext
    request_id: int
    file_id: int
    
class SXRayFile(SXRayFileAdd):
    id: int

class SXRayFileRel(SXRayFile):
    request: "SXRayRequest"
    file_data: "SFile"
    predict: "SXRayImagePredicted"
    
class SXRayRequestRel(SXRayRequest):
    xray_files: list["SXRayFile"]
    

class SXRayImagePredictedAdd(BaseModel):
    xray_file_id: int
    predicted_at: datetime

class SXRayImagePredicted(SXRayImagePredictedAdd):
    id: int
    
class SXRayImagePredictedRel(SXRayImagePredicted):
    xray_file: "SXRayFile"
    classes: list["SPredictedClass"]

class SPredictedClassAdd(BaseModel):
    xray_predict_id: int
    class_id: int
    
class SPredictedClass(BaseModel):
    id: int

class SPredictedClassRel(SPredictedClass):
    predict: "SXRayImagePredicted"
    class_info: "SPredictedClasses"

