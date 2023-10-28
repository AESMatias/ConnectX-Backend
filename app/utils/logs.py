from app.models.user import User as ModelUser
from datetime import datetime
from app.models.user import UserAccountLogs as ModelAccountLogs
from sqlalchemy.orm import Session

data_time = datetime.now()


def log_action_user(db: Session, action: str, user_name: str):
    user = db.query(ModelUser).filter_by(username=user_name).first()
    log = ModelAccountLogs(user_id=user.id, log=f"{action}", log_at=data_time)
    if not db.is_active:
        with db.begin() as conn:
            conn.add(log)
            conn.commit()
            conn.refresh(log)
            user.updated_at = data_time
            conn.commit()
            conn.refresh(user)
    else:
        db.add(log)
        db.commit()
        db.refresh(log)
        user.updated_at = data_time
        db.commit()
        db.refresh(user)
    return True
