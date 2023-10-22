from fastapi import UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.config.db import get_db
from app.models.user import ProfileImage as DBProfileImage
from app.schemas.images import ProfileImage 
from fastapi import APIRouter, HTTPException
from app.utils.auth import get_current_user
from app.models.user import User as ModelUser
from app.config.db import get_db
from PIL import Image
from io import BytesIO
from datetime import datetime
images = APIRouter()

import os

@images.post("/uploadfile/")
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
    return FileResponse (f"Data/profile_pics/{current_user.username}/RAW/{user_id}-{user_name}-{current_time}.png")


@images.get("/profilePIC/")
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
    return FileResponse(f"Data/profile_pics/{current_user.username}/{current_user.username}.png")
