from pydantic import BaseModel
from typing import List

class SXrayMessageRequest(BaseModel):
    # request_id: int
    xray_file_id: int


class SXrayMessageResponse(SXrayMessageRequest):
    predicted_class: List[int]
