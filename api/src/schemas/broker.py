from pydantic import BaseModel
from typing import List

class SXrayMessageRequest(BaseModel):
    xray_file_id: int
    aws_path: str


class SXrayMessageResponse(SXrayMessageRequest):
    predicted_class: List[int]
    aws_path: str | None
