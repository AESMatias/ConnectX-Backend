from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.config.db import SessionLocal
from app.models.user import User as ModelUser
from app.models.user import ProfileImage as DBProfileImage
from sqlalchemy import desc

def user_from_db(user_name:str, db:Session):
    if not db.is_active:
        with db.begin() as conn:
            user = conn.query(ModelUser).filter_by(username=user_name).first()
            conn.close()
    else:
        db = SessionLocal()
        user = db.query(ModelUser).filter_by(username=user_name).first()
        db.close()
    return user

def post_user_to_db(user, db:Session):
    if not db.is_active:
        with db.begin() as conn:
            conn.add(user)
            conn.commit()
            conn.refresh(user)
            conn.close()
    else:
        db = SessionLocal()
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
    return True
def get_profile_image_by_id(current_user_id,db:Session):
    if not db.is_active:
        with db.begin() as conn:
            profile_image = conn.query(DBProfileImage).filter_by(user_id=current_user_id).order_by(desc(DBProfileImage.upload_at)).first()
            conn.close()
    else:
        db = SessionLocal()
        profile_image = db.query(DBProfileImage).filter_by(user_id=current_user_id).order_by(desc(DBProfileImage.upload_at)).first()
        db.close()
    if profile_image is None:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    return profile_image

def post_profile_image_by_id(current_user_id, blob_data, data_time, db:Session):
    if not db.is_active:
        with db.begin() as conn:
            profile_image = DBProfileImage(user_id=current_user_id, image=blob_data, upload_at=data_time)
            conn.add(profile_image)
            conn.commit()
            conn.close()
    else:
        db = SessionLocal()
        profile_image = DBProfileImage(user_id=current_user_id, image=blob_data, upload_at=data_time)
        db.add(profile_image)
        db.commit()
        db.close()
    return True

