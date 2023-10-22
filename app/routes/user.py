from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from app.models.user import User as ModelUser
from app.models.user import ProfileImage as DBProfileImage
from app.schemas.user import User as SchemaUser
from app.schemas.user import UserNameUpdate as SchemaUserUpdate
from app.schemas.user import UserPasswordUpdate as SchemaUserPassUpdate
from app.schemas.user import Response as SchemaResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.config.db import get_db
from app.utils.auth import get_password_hash
from app.utils.auth import get_user_by_name
from app.utils.auth import get_current_user
from app.utils.logs import log_action_user
from PIL import Image
from io import BytesIO
from datetime import datetime
import os


user = APIRouter()


@user.get("/user/{user_name}", response_model= SchemaUser, tags=["self"])
def get_user(user_name: str, db: Session = Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        return get_user_by_name(user_name, db)
    elif current_user.username == user_name:
        return get_user_by_name(user_name, db)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@user.get("/user/profilePIC/", tags=["self"])
async def profile_pic(
        current_user: ModelUser = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    profile_image = db.query(DBProfileImage).filter_by(user_id=current_user.id).order_by(desc(DBProfileImage.upload_at)).first()
    image = Image.open(BytesIO(profile_image.image))
    image.thumbnail((200, 200))
    try:
        os.makedirs(f"Data/profile_pics/{current_user.username}")
    except FileExistsError:
        pass
    image.save(f"Data/profile_pics/{current_user.username}/{current_user.username}.png", "PNG")
    log_action_user(action=f"User {current_user.username} get profile picture", user_name=current_user.username)
    return FileResponse(f"Data/profile_pics/{current_user.username}/{current_user.username}.png")


@user.post("/user/profilePIC/upload", tags=["self"])
async def create_upload_file(
    file: UploadFile = File(...),
    current_user: ModelUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    user_name = current_user.username
    current_time = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    data_time = datetime.now()
    try:
        os.makedirs(f"Data/profile_pics/{current_user.username}/RAW")
    except FileExistsError:
        pass
    with Image.open(file.file) as img:
        try:
            os.makedirs(f"Data/profile_pics/{current_user.username}/RAW")
        except FileExistsError:
            pass
        img.save(f"Data/profile_pics/{current_user.username}/RAW/{user_id}-{user_name}-{current_time}.png", "PNG")
    with open(f"Data/profile_pics/{current_user.username}/RAW/{user_id}-{user_name}-{current_time}.png", 'rb') as f:
        blob_data = f.read()
    profile_image = DBProfileImage(user_id=user_id, image=blob_data, upload_at=data_time)
    db.add(profile_image)
    db.commit()
    log_action_user(action=f"User {current_user.username} uploaded a profile picture", user_name=current_user.username)
    return FileResponse (f"Data/profile_pics/{current_user.username}/RAW/{user_id}-{user_name}-{current_time}.png")


@user.post("/Register", response_model= SchemaResponse, tags=["auth"])
def created_users(entry:SchemaUser,db:Session=Depends(get_db)):
    password_hashed = get_password_hash(entry.password)
    entry_admin = False
    if entry.username == "admin" or entry.username == "Admin" or entry.username == "ADMIN":
        entry_admin = True
    user = ModelUser(
        username = entry.username,
        password = password_hashed,
        created_at = entry.created_at,
        updated_at = entry.updated_at,
        admin = entry_admin,
        banned = False,
        disabled = False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    catch_user = db.query(ModelUser).filter_by(username=entry.username).first()
    log_action_user(action=f"User {catch_user.username} created", user_name=catch_user.username)
    response = SchemaResponse(mensage="User Created")
    return response

@user.put("/user/updatepass", response_model= SchemaResponse, tags=["self"])
def update_pass(entry:SchemaUserPassUpdate, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    password_hashed = get_password_hash(entry.password)
    user = db.query(ModelUser).filter_by(username=current_user.username).first()
    user.password = password_hashed
    db.commit()
    db.refresh(user)
    log_action_user(action=f"User {user.username} updated password", user_name=user.username)
    response = SchemaResponse(mensage="Password Updated")
    return response

@user.put("/user/updatename/", response_model= SchemaResponse, tags=["self"])
def update_name(entry:SchemaUserUpdate, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    user = db.query(ModelUser).filter_by(username=current_user.username).first()
    new_name = entry.username
    log_action_user(action=f"User {user.username} updated name to {new_name}", user_name=user.username)
    user.username = new_name
    db.commit()
    db.refresh(user)
    response = SchemaResponse(mensage="Relog to see changes")
    return response

@user.delete("/user/delete", response_model= SchemaResponse, tags=["self"])
def delete_users(db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    user_id = current_user.id
    user = db.query(ModelUser).filter_by(id=user_id).first()
    user.disabled = True
    db.commit()
    log_action_user(action=f"User {user.username} deleted by self", user_name=user.username)
    response = SchemaResponse(mensage = "Your account pass away")
    return response