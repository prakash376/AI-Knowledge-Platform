from datetime import datetime
from pydantic import BaseModel


class DocumentOut(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True