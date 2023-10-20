from fastapi import APIRouter, Depends
from app.models.user import User as ModelUser
from app.schemas.user import User as SchemaUser
from app.schemas.user import UserNameUpdate as SchemaUserUpdate
from app.schemas.user import UserPasswordUpdate as SchemaUserPassUpdate
from app.schemas.user import Response as SchemaResponse
from app.schemas.user import UserID as SchemaUserID
from typing import List
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.utils.auth import get_password_hash
from app.utils.auth import get_user_by_name

user = APIRouter()


@user.get("/users", response_model= List[SchemaUser])
def show_users(db:Session=Depends(get_db)):
    users = db.query(ModelUser).all()
    return users

@user.get("/idbyname", response_model= SchemaUserID)
def getId(user_name:str,db:Session=Depends(get_db)):
    user = db.query(ModelUser).filter_by(username= user_name).first()
    return user


@user.get("/user/{user_name}", response_model= SchemaUser)
def get_user(user_name:str,db:Session=Depends(get_db)):
    return get_user_by_name(user_name, db)

@user.post("/user", response_model= SchemaUser)
def created_users(entry:SchemaUser,db:Session=Depends(get_db)):
    passwordhash = get_password_hash(entry.password)
    user = ModelUser(username = entry.username, password = passwordhash, disabled = False, created_at = entry.created_at)
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