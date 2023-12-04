from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User as ModelUser
from app.schemas.user import User as SchemaUser
from app.schemas.user import Response as SchemaResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.config.db import get_db
from app.config.db import Base
from app.utils.auth import get_current_user
from app.utils.logs import log_action_user
from app.utils.db import user_from_db
from app.utils.db import post_user_to_db
from typing import List


admin = APIRouter()


@admin.get("/admin/show_users", response_model=List[SchemaUser], tags=["admin"])
def show_users(current_user: ModelUser = Depends(get_current_user),
               db: Session = Depends(get_db)
               ):
    if current_user.admin:
        users = db.query(ModelUser).order_by(desc(ModelUser.created_at)).limit(100).all()
        db.close()
        log_action_user(db, action=f"Show Last 100 Users by {current_user.username}", user_name=current_user.username)
        return users
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")


@admin.put("/admin/range/{user_name}", response_model= SchemaResponse, tags=["admin"])
def range_any_user(user_name: str, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        user = user_from_db(user_name=user_name, db=db)
        if user:
            user.admin = True
            post_user_to_db(user=user, db=db)
            response = SchemaResponse(message="User promoted")
            log_action_user(db, action=f"Promote {user_name} to admin by {current_user.username}", user_name=current_user.username)
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@admin.put("/admin/ban/{user_name}", response_model= SchemaResponse, tags=["admin"])
def ban_any_user(user_name: str, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        user = user_from_db(user_name=user_name, db=db)
        if user:
            user.banned = True
            post_user_to_db(user=user, db=db)
            response = SchemaResponse(message=f"User {user.username} banned by {current_user.username}")
            log_action_user(db, action=f"Ban {user_name}", user_name=current_user.username)
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@admin.put("/admin/unban/{user_name}", response_model= SchemaResponse, tags=["admin"])
def unban_any_user(user_name: str, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        user = user_from_db(user_name=user_name, db=db)
        if user:
            user.banned = False
            post_user_to_db(user=user, db=db)
            response = SchemaResponse(message="User unbanned")
            log_action_user(db, action=f"User {user.username} unbanned by {current_user.username}", user_name=current_user.username)
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@admin.delete("/admin/delete/{user_name}", response_model= SchemaResponse, tags=["admin"])
def delete_any_user(user_name: str, db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        user = user_from_db(user_name=user_name, db=db)
        if user:
            user.disabled = True
            post_user_to_db(user=user, db=db)
            response = SchemaResponse(message="User deleted")
            log_action_user(db, action=f"Disable {user_name} account by {current_user.username}", user_name=current_user.username)
            return response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@admin.delete("/admin/tables/delete", response_model= SchemaResponse, tags=["admin"])
def delete_tables(db:Session=Depends(get_db), current_user: ModelUser = Depends(get_current_user)):
    if current_user.admin:
        Base.metadata.drop_all(bind=db.bind)  # Esta línea elimina todas las tablas
        db.close()
        return {"message": "All tables deleted"}
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")