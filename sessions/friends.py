from fastapi import APIRouter, Depends
from app.models.user import Friends
from app.config.db import SessionLocal
from app.utils.db import user_from_db
from app.models.user import User as ModelUser
from app.config.db import get_db
from app.utils.auth import get_current_user
from sqlalchemy.orm import Session

friend = APIRouter()

def friend_from_db(id: int, db: Session):
    friends = db.query(Friends).filter(Friends.iduser == id,
                                       Friends.accepted == True).all()
    return friends

@friend.post("/friend/request", tags=["friends"])
def send_friend_request(username: str,
                        db: Session = Depends(get_db),
                        current_user: ModelUser = Depends(get_current_user)):
    user_id = current_user.id
    friend = Friends(iduser=user_id,
                     username=username,
                     accepted=False,
                     pendient=True,
                     rejected=False)
    db.add(friend)
    db.commit()
    db.refresh(friend)
    return friend

@friend.put("/friend/request/accept", tags=["friends"])
def accept_friend_request(username: str,
                          db: Session = Depends(get_db),
                          current_user: ModelUser = Depends(get_current_user)):
    user_id = current_user.id
    friend = db.query(Friends).filter(Friends.iduser == user_id,
                                      Friends.username == username).first()
    friend.accepted = True
    friend.pendient = False
    db.commit()
    db.refresh(friend)
    return friend

@friend.put("/friend/request/reject", tags=["friends"])
def reject_friend_request(username: str,
                          db: Session = Depends(get_db),
                          current_user: ModelUser = Depends(get_current_user)):
    user_id = current_user.id
    friend = db.query(Friends).filter(Friends.iduser == user_id,
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
    user_id = current_user.id
    friends = friend_from_db(user_id, db)
    return friends
