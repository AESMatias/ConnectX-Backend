from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, LargeBinary, Boolean
from sqlalchemy.orm import relationship
from app.config.db import Base , engine


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime)
    disabled = Column(Boolean)

class UserFile(Base):
    __tablename__ = 'user_files'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file = Column(LargeBinary)
    created_at = Column(DateTime)

    user = relationship("User", back_populates="user_files")

User.user_files = relationship("UserFile", back_populates="user")






Base.metadata.create_all(engine)
