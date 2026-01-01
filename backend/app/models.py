from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String(30), unique=True, nullable=False)
	hashed_pwd = Column(Text, nullable=False)
	posts = relationship("Post", back_populates="owner")


class Post(Base):
	__tablename__ = "posts"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(100), nullable=False)
	content = Column(Text, nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	owner_id = Column(Integer, ForeignKey("users.id"))
	owner = relationship("User", back_populates="posts")
