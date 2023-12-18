from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import Message
from app.config.db import SessionLocal
from app.models.user import User

def post_message(user_id, message_text):
    db = SessionLocal()

    # Verifica si el usuario existe antes de insertar el mensaje
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        message = Message(iduser=user_id, mensaje=message_text, datatime=datetime.now())
        db.add(message)
        db.commit()
        db.close()
        return True
    else:
        # El usuario no existe, puedes manejar esto según tus necesidades
        db.close()
        return False
# Ejemplo de uso
current_user_id = 1  # Reemplaza con el ID de usuario adecuado
message_text = "Hola, este es un mensaje de ejemplo."
post_message(current_user_id, message_text)

