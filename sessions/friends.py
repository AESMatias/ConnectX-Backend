from fastapi import APIRouter, Depends
from app.models.user import Friends
from app.config.db import SessionLocal
from app.utils.db import user_from_db
from app.models.user import User as ModelUser
from app.config.db import get_db
from app.utils.auth import get_current_user
from sqlalchemy.orm import Session
from app.utils.db import user_name_from_db
friend = APIRouter()


@friend.post("/friend/request", tags=["friends"])
def send_friend_request(username: str,
                        db: Session = Depends(get_db),
                        current_user: ModelUser = Depends(get_current_user)):
    user_id = current_user.id
    username = username
    friend = db.query(Friends).filter(Friends.iduser == user_id,
                                      Friends.username == username).first()
    if friend:
        friend = Friends(iduser=user_id, username=username, accepted=False ,pendient=True, rejected=False)
        db.add(friend)
        db.commit()
        db.refresh(friend)
        return friend
    friend = Friends(iduser=user_id, username=username, accepted=False ,pendient=True, rejected=False)
    db.add(friend)
    db.commit()
    db.refresh(friend)
    return friend


@friend.put("/friend/request/accept", tags=["friends"])
def accept(username: str,
                          db: Session = Depends(get_db),
                          current_user: ModelUser = Depends(get_current_user)):
    userid = user_from_db(username, db).id
    username = current_user.username
    #filtrar solicitud por id, iduser y username
    friend = db.query(Friends).filter(Friends.iduser == userid,
                                      Friends.username == username).first()
    friend.accepted = True
    friend.pendient = False
    friend.rejected = False
    db.commit()
    db.refresh(friend)
    return friend

@friend.put("/friend/request/reject", tags=["friends"])
def reject_friend_request(username: str,
                          db: Session = Depends(get_db),
                          current_user: ModelUser = Depends(get_current_user)):
    userid = user_from_db(username, db).id
    username = current_user.username
    friend = db.query(Friends).filter(Friends.iduser == userid,
                                      Friends.username == username).first()
    friend.accepted = False
    friend.pendient = False
    friend.rejected = True
    db.commit()
    db.refresh(friend)
    return friend


@friend.get("/friends", tags=["friends"])
def get_friends(db: Session = Depends(get_db),
                current_user: ModelUser = Depends(get_current_user)):
    user_name = current_user.username
    friends = db.query(Friends).filter(Friends.username == user_name,
                                       Friends.accepted == True).all()
    amigos = []
    for friend in friends:
        amigos.append(user_name_from_db(friend.iduser, db))
    return amigos




@friend.get("/friends/pendient", tags=["friends"])
def get_friends(db: Session = Depends(get_db),
                current_user: ModelUser = Depends(get_current_user)):
    user_name = current_user.username
    friends = db.query(Friends).filter(Friends.username == user_name,
                                       Friends.pendient == True).all()
    amigos = []
    for friend in friends:
        amigo_dict = {
            'username': user_name_from_db(friend.iduser, db),
            'accepted': friend.accepted,
            'pendient': friend.pendient,
            'rejected': friend.rejected
        }
        amigos.append(amigo_dict)
    return amigos
