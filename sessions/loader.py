from sqlalchemy import or_, and_, desc
from datetime import datetime
from app.models.user import Message
from app.models.user import MessageP2P
from app.config.db import SessionLocal
from sqlalchemy import desc
from app.utils.db import user_from_db
def post_message_to_general(username, message_text):
    db = SessionLocal()
    user = user_from_db(username,db)
    user_id = user.id
    message = Message(iduser=user_id, mensaje=message_text, datatime=datetime.now())
    db.add(message)
    db.commit()
    db.close()
    return True

def post_message_to_chat():
    db = SessionLocal()
    messages = db.query(Message).order_by(desc(Message.datatime)).limit(50).all()
    db.close()
    return messages

def message_p2p(user1, user2, message_text):
    db = SessionLocal()
    user1 = user_from_db(user1, db)
    user2 = user_from_db(user2, db)
    user1id = user1.id
    user2id = user2.id
    message = MessageP2P(mensaje=message_text, iduser1=user1id, iduser2=user2id,datatime=datetime.now())
    db.add(message)
    db.commit()
    db.close()
    return True

def post_message_to_chat_p2p(user_id_1, user_id_2):
    db = SessionLocal()
    try:
        messages = (
            db.query(MessageP2P)
            .filter(
                or_(
                    and_(MessageP2P.iduser1 == user_id_1, MessageP2P.iduser2 == user_id_2),
                    and_(MessageP2P.iduser1 == user_id_2, MessageP2P.iduser2 == user_id_1),
                )
            )
            .order_by(desc(MessageP2P.id))
            .limit(50)
            .all()
        )
        return messages
    finally:
        db.close()