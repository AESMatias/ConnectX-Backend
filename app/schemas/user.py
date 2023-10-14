from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    created_at: Optional[datetime] = datetime.now()
    state: int

    class Config:
        orm_mode = True


class UserNameUpdate(BaseModel):
    username: str

    class Config:
        orm_mode = True

class UserPasswordUpdate(BaseModel):
    password: str

    class Config:
        orm_mode = True

class UserID(BaseModel):
    id: int

    class Config:
        orm_mode = True

class Response(BaseModel):
    mensage: str
