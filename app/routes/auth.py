from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth import authenticate_user
from app.utils.auth import create_access_token
from app.utils.auth import get_current_active_user
from app.utils.auth import get_current_user_by_token
from app.utils.logs import log_action_user
from app.schemas.user import Token
from app.schemas.user import User
from app.config.db import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from datetime import timedelta
from typing import Annotated
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)

auth = APIRouter()

@auth.post("/token", response_model=Token, tags=["auth"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.banned:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User banned",
            headers={"WWW-Authenticate": "Bearer"},
        )
    log_action_user(db=db, action=f"{form_data.username} Logged In", user_name=form_data.username)
    log_action_user(db=db, action=f"{form_data.username} token timeout {datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}", user_name=user.username)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@auth.get("/users/me/", response_model=User, tags=["auth"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@auth.get("/users/me/items/" , tags=["root"])
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

#QandA
# https://fastapi.tiangolo.com/tutorial/security/