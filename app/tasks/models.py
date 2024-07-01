from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from auth.models import User
from datetime import datetime


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.tg_id'))
    user = relationship("User", back_populates="tasks")

User.tasks = relationship("Task", order_by=Task.id, back_populates="user")
