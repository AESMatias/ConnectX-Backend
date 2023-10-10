from fastapi import APIRouter, HTTPException, Depends
from config.db import conn
from models.user import users
from schemas.user import User, UserLogin
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from config.db import get_db
import os

user = APIRouter()

if not os.path.exists("secret.key"):
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
else:
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
fpass = Fernet(key)

@user.post('/users')
def create_user(user: User ):
    new_user = {"nickName": user.nickName}
    new_user["password"] = fpass.encrypt(user.password.encode("utf-8"))
    print(new_user)
    result = conn.execute(users.insert().values(**new_user))
    conn.commit()
    return new_user



@user.post('/get_user_id')
def get_user_id(nickName: str, db: Session = Depends(get_db)):
    result = db.query(User.id).filter(User.nickName == nickName).first()
    if result:
        return {"id": result.id}
    else:
        return {"message": "User not found"}


@user.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = db.query(User.id, User.nickName, User.password, User.creationDate, User.sessionState).filter(User.nickName == user.nickName).first()
    if result:
        # El usuario existe, verificar la contraseña
        if fpass.decrypt(result.password).decode("utf-8") == user.password:
            # La contraseña es correcta, hacer algo aquí
            return {"message": "Login successful"}
        else:
            # La contraseña es incorrecta
            return {"message": "Incorrect password"}
    else:
        # El usuario no existe
        return {"message": "User not found"}