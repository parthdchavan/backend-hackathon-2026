from pydantic import BaseModel
from datetime import datetime

class ObjectionCreate(BaseModel):
    objection_text: str

class ObjectionResponse(BaseModel):
    id: int
    objection_text: str
    response: str
    category: str
    severity: str
    created_at: datetime

    class Config:
        from_attributes = True
