from fastapi import UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.user import ProfileImage as DBProfileImage
from app.schemas.images import ProfileImage 
from fastapi import APIRouter, HTTPException
from app.utils.auth import get_current_user
from app.models.user import User as ModelUser
from app.config.db import get_db
from PIL import Image
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
        os.makedirs("Data/raw_profile_pics")
    except FileExistsError:
        pass
    with Image.open(file.file) as img:
        img.save(f"Data/raw_profile_pics/{user_id}-{user_name}-{current_time}.png", "PNG")
    with open(f"Data/raw_profile_pics/{user_id}-{user_name}-{current_time}.png", 'rb') as f:
        blob_data = f.read()
    profile_image = DBProfileImage(user_id=user_id, image=blob_data, upload_at=data_time)
    db.add(profile_image)
    db.commit()
    return {"file_name": f"{user_name}{user_id}{current_time}", "user": user_name}