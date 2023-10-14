from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserFile(BaseModel):
    id: Optional[int] = None
    user_id: int
    file: bytes
    created_at: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True