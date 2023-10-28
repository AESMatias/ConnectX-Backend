from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from app.models.user import User as ModelUser
from app.schemas.user import User as SchemaUser
from app.schemas.user import UserNameUpdate as SchemaUserUpdate
from app.schemas.user import UserPasswordUpdate as SchemaUserPassUpdate
from app.schemas.user import Response as SchemaResponse
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.utils.auth import get_password_hash
from app.utils.auth import get_user_by_name
from app.utils.auth import get_current_user
from app.utils.logs import log_action_user
from app.utils.db import user_from_db
from app.utils.db import post_user_to_db
from app.utils.db import get_profile_image_by_id
from app.utils.db import post_profile_image_by_id

from PIL import Image
from io import BytesIO
from datetime import datetime
import os


user = APIRouter()


@user.get("/user/{user_name}", response_model= SchemaUser, tags=["self"])
def get_user(user_name: str, db: Session = Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if not log_action_user(db, action=f"User {current_user.username} get info about: {user_name}", user_name=current_user.username):
        raise HTTPException(status_code=500, detail="Failed to log action")
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
    profile_image = get_profile_image_by_id(current_user.id, db)
    image = Image.open(BytesIO(profile_image.image))
    image.thumbnail((200, 200))
    try:
        os.makedirs(f"Data/profile_pics/{current_user.username}")
    except FileExistsError:
        pass
    image.save(f"Data/profile_pics/{current_user.username}/{current_user.username}.png", "PNG")
    if not log_action_user(db, f"User {current_user.username} get profile picture", user_name=current_user.username):
        raise HTTPException(status_code=500, detail="Failed to log action")
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
    post_profile_image_by_id(user_id, blob_data, data_time, db)
    if not log_action_user(db, action=f"User {current_user.username} uploaded a profile picture", user_name=current_user.username):
        raise HTTPException(status_code=500, detail="Failed to log action")
    return FileResponse (f"Data/profile_pics/{current_user.username}/RAW/{user_id}-{user_name}-{current_time}.png")


@user.post("/Register", response_model= SchemaResponse, tags=["auth"])
async def created_users(entry: SchemaUser, db: Session = Depends(get_db)):
    password_hashed = get_password_hash(entry.password)
    entry_admin = False
    user_exist = user_from_db(entry.username, db)
    if len(entry.username) > 20:
        raise HTTPException(status_code=403, detail="Username too long")
    if user_exist:
        raise HTTPException(status_code=403, detail="User already exists")
    if entry.username.lower() == "admin":
        entry_admin = True
    user = ModelUser(
        username=entry.username,
        password=password_hashed,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
        admin=entry_admin,
        banned=False,
        disabled=False
    )
    post_user_to_db(user, db)
    string_name = entry.username
    if not log_action_user(db, action=f"User {entry.username} created", user_name=string_name):
        raise HTTPException(status_code=500, detail="Failed to log action")

    response = SchemaResponse(message="User Created")
    return response

@user.put("/user/updatepass", response_model= SchemaResponse, tags=["self"])
def update_pass(entry:SchemaUserPassUpdate, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    password_hashed = get_password_hash(entry.password)
    user = user_from_db(current_user.username, db)
    user.password = password_hashed
    post_user_to_db(user, db)
    if not log_action_user(db, action=f"User {user.username} updated password", user_name=user.username):
        raise HTTPException(status_code=500, detail="Failed to log action")
    response = SchemaResponse(message="Password Updated")
    return response

@user.put("/user/updatename/", response_model= SchemaResponse, tags=["self"])
def update_name(entry:SchemaUserUpdate, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    user = user_from_db(current_user.username, db)
    new_name = entry.username
    user.username = new_name
    post_user_to_db(user, db)
    if not log_action_user(db, action=f"User {user.username} updated name to {new_name}", user_name=user.username):
        raise HTTPException(status_code=500, detail="Failed to log action")
    response = SchemaResponse(message="Relog to see changes")
    return response

@user.delete("/user/delete", response_model= SchemaResponse, tags=["self"])
def delete_users(db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    user_name = current_user.username
    user = user_from_db(user_name, db)
    user.disabled = True
    post_user_to_db(user, db)
    if not log_action_user(db, action=f"User {user.username} deleted by self", user_name=user.username):
        raise HTTPException(status_code=500, detail="Failed to log action")
    response = SchemaResponse(message = "Your account pass away")
    return response