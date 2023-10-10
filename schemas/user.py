from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserLogin(BaseModel):
    nickName: str
    password: str

class User(BaseModel):
    id: Optional[int] = None
    nickName: str
    password: str
    creationDate: datetime = datetime.utcnow()
    sessionState: bool = False