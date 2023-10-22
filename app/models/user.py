from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, LargeBinary, Boolean
from sqlalchemy.orm import relationship
from app.config.db import Base , engine
from sqlalchemy.orm import Session


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    disabled = Column(Boolean)

class ProfileImage(Base):
    __tablename__ = 'profile_images'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    image = Column(LargeBinary(length=4000000000))
    upload_at = Column(DateTime)

    user = relationship("User", back_populates="profile_images")

User.profile_images = relationship("ProfileImage", back_populates="user")





Base.metadata.create_all(engine)
