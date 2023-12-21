from sqlalchemy import or_, and_, desc
from datetime import datetime
from app.models.user import Message
from app.models.user import Messagep2p
from app.config.db import SessionLocal
from sqlalchemy import desc
from app.utils.db import user_from_db


def post_message_to_general(username, message_text):
    db = SessionLocal()
    user = user_from_db(username,db)
    user_id = user.id
    username = user.username
    message = Message(iduser=user_id,username= username, mensaje=message_text, datatime=datetime.now())
    db.add(message)
    db.commit()
    db.close()
    return True

def post_message_to_chat():
    db = SessionLocal()
    messages = db.query(Message).order_by(desc(Message.datatime)).limit(50).all()
    db.close()
    return messages

def post_message_to_p2p(username, message_text, username2):
    db = SessionLocal()
    user = user_from_db(username,db)
    user_id = user.id 
    username = user.username
    message = Messagep2p(iduser=user_id,username= username,username2=username2, mensaje=message_text, datatime=datetime.now())
    db.add(message)
    db.commit()
    db.close()
    return True