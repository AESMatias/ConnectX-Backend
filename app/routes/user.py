from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User as ModelUser
from app.schemas.user import User as SchemaUser
from app.schemas.user import UserNameUpdate as SchemaUserUpdate
from app.schemas.user import UserPasswordUpdate as SchemaUserPassUpdate
from app.schemas.user import Response as SchemaResponse
from app.schemas.user import UserID as SchemaUserID
from typing import List
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from app.config.db import get_db
import os

user = APIRouter()

if not os.path.exists("secret.key"):
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
else:
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
fpass = Fernet(key)

@user.get("/users", response_model= List[SchemaUser])
def show_users(db:Session=Depends(get_db)):
    users = db.query(ModelUser).all()
    return users

@user.get("/idbyname", response_model= SchemaUserID)
def getId(user_name:str,db:Session=Depends(get_db)):
    user = db.query(ModelUser).filter_by(username= user_name).first()
    return user


@user.post("/user", response_model= SchemaUser)
def created_users(entry:SchemaUser,db:Session=Depends(get_db)):
    user = ModelUser(username = entry.username, password = entry.password, state = entry.state, created_at = entry.created_at)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@user.put("/user/pass/{user_id}", response_model= SchemaUser)
def update_pass(user_id: int, entry:SchemaUserPassUpdate,db:Session=Depends(get_db)):
    user = db.query(ModelUser).filter_by(id=user_id).first()
    user.password = entry.password
    db.commit()
    db.refresh(user)
    return user

@user.put("/user/name/{user_id}", response_model= SchemaUser)
def update_users(user_id: int, entry:SchemaUserUpdate,db:Session=Depends(get_db)):
    user = db.query(ModelUser).filter_by(id=user_id).first()
    user.username = entry.username
    db.commit()
    db.refresh(user)
    return user

@user.delete("/user/{user_id}", response_model= SchemaResponse)
def delete_users(user_id: int,db:Session=Depends(get_db)):
    user = db.query(ModelUser).filter_by(id=user_id).first()
    db.delete(user)
    db.commit()
    response = SchemaResponse(mensage = "User deleted")
    return response