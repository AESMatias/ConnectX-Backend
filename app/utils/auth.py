from typing import Annotated
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.config.db import SessionLocal
from app.models.user import User as ModelUser
from app.schemas.user import TokenData
from app.schemas.user import User
from app.schemas.user import UserInDB
from decouple import config
from app.utils.db import user_from_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)

def get_user_by_name(user_name:str, db:Session):
    user = user_from_db(user_name, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


#verify_password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
#get_password_hash
def get_password_hash(password):
    return pwd_context.hash(password)
#get_user
def get_user(username: str):
    db = SessionLocal()
    user = get_user_by_name(username, db)
    if user:
        return UserInDB(**user.__dict__)
    return None
#authenticate_user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        False
    if not verify_password(password, user.password):
        return False
    return user
#create_access_token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
#Async get_current_user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
#Async get_current_active_user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
