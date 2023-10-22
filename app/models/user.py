from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, LargeBinary, Boolean
from sqlalchemy.orm import relationship
from app.config.db import Base, engine
from sqlalchemy.orm import Session


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    admin = Column(Boolean)
    banned = Column(Boolean)
    disabled = Column(Boolean)

    profile_images = relationship("ProfileImage", back_populates="user")
    user_account_logs = relationship("UserAccountLogs", back_populates="user")

class ProfileImage(Base):
    __tablename__ = 'profile_images'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    image = Column(LargeBinary(length=4000000000))
    upload_at = Column(DateTime)

    user = relationship("User", back_populates="profile_images")

class UserAccountLogs(Base):
    __tablename__ = 'user_account_logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    log = Column(String(255))
    log_at = Column(DateTime)

    user = relationship("User", back_populates="user_account_logs")

User.user_account_logs = relationship("UserAccountLogs", back_populates="user")
User.profile_images = relationship("ProfileImage", back_populates="user")




Base.metadata.create_all(engine)
