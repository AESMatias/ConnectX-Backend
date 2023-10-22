from app.models.user import User as ModelUser
from datetime import datetime
from app.config.db import SessionLocal
from app.models.user import UserAccountLogs as ModelAccountLogs


db = SessionLocal()
data_time = datetime.now()
def log_action_user(action: str, user_name: str):
    user = db.query(ModelUser).filter_by(username=user_name).first()
    log = ModelAccountLogs(user_id=user.id, log=f"{action}", log_at=data_time)
    db.add(log)
    db.commit()
    db.refresh(log)
    user.updated_at = data_time
    db.commit()
    db.refresh(user)

