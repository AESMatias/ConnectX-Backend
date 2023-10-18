from typing import Optional, Union
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    created_at: Optional[datetime] = datetime.now()
    disabled: bool | None = None

    class Config:
        orm_mode = True

class SchemaLogin(BaseModel):
    username: str
    password: str

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

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    password: str