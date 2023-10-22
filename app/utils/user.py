from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.models.user import User as ModelUser
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.utils.auth import get_current_user
from datetime import datetime
import os
#funcion de referencia no util
async def update_logs(current_user: ModelUser = Depends(get_current_user), db: Session = Depends(get_db)):
    data_time = datetime.now()
    user = db.query(ModelUser).filter_by(username=current_user.username).first()
    user.updated_at = data_time
    db.commit()
    db.refresh(user)


data_time = datetime.now()
log = ModelAccountLogs(user_id=current_user.id, log=f"Unban {user_name} by {current_user.username}", log_at=data_time)
db.add(log)
db.commit()
db.refresh(log)
user = db.query(ModelUser).filter_by(username=current_user.username).first()
user.updated_at = data_time
db.commit()
db.refresh(user)