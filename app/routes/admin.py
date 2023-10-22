from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User as ModelUser
from app.schemas.user import User as SchemaUser
from app.schemas.user import Response as SchemaResponse
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.utils.auth import get_current_user
from app.utils.logs import log_action_user
from typing import List


admin = APIRouter()


@admin.get("/admin/show_users", response_model= List[SchemaUser], tags=["admin"])
def show_users(current_user: ModelUser = Depends(get_current_user),
               db:Session=Depends(get_db)
               ):
    if current_user.admin:
        users = db.query(ModelUser).all()
        log_action_user(action=f"Show All Users by {current_user.username}", user_name=current_user.username)
        return users
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")


@admin.put("/admin/range/{user_name}", response_model= SchemaResponse, tags=["admin"])
def range_any_user(user_name: str, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        user = db.query(ModelUser).filter_by(username=user_name).first()
        if user:
            user.admin = True
            db.commit()
            response = SchemaResponse(mensage="User promoted")
            log_action_user(action=f"Promote {user_name} to admin by {current_user.username}", user_name=current_user.username)
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@admin.put("/admin/ban/{user_name}", response_model= SchemaResponse, tags=["admin"])
def ban_any_user(user_name: str, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        user = db.query(ModelUser).filter_by(username=user_name).first()
        if user:
            user.banned = True
            db.commit()
            response = SchemaResponse(mensage=f"User {user.username} banned by {current_user.username}")
            log_action_user(action=f"Ban {user_name}", user_name=current_user.username)
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@admin.put("/admin/unban/{user_name}", response_model= SchemaResponse, tags=["admin"])
def unban_any_user(user_name: str, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        user = db.query(ModelUser).filter_by(username=user_name).first()
        if user:
            user.banned = False
            db.commit()
            response = SchemaResponse(mensage="User unbanned")
            log_action_user(action=f"User {user.username} unbanned by {current_user.username}", user_name=current_user.username)
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@admin.delete("/admin/delete/{user_name}", response_model= SchemaResponse, tags=["admin"])
def delete_any_user(user_name: str, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        user = db.query(ModelUser).filter_by(username=user_name).first()
        if user:
            user.disabled = True
            db.commit()
            response = SchemaResponse(mensage="User deleted")
            log_action_user(action=f"Disable {user_name} account by {current_user.username}", user_name=current_user.username)
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
