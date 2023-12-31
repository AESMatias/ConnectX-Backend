from typing import Optional, Union
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    admin: bool | None = False
    banned: bool | None = False
    disabled: bool | None = False

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
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    password: str