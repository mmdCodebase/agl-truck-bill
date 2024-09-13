from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class TruckBillEmailAttachment(BaseModel):
    id: Optional[int] = None
    attachment_id: Optional[str] = None
    email_id: Optional[str] = None
    file_name: Optional[str] = None
    content_type: Optional[str] = None
    is_inline: Optional[bool] = None

    class Config:
        from_attributes=True

class TruckBillEmail(BaseModel):
    email_id: Optional[str] = None
    attachments: Optional[List[TruckBillEmailAttachment]] = None
