from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ProfileImage(BaseModel):
    id: Optional[int] = None
    user_id: int
    image: bytes
    upload_at: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True