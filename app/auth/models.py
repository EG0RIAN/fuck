from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    tg_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    language_code = Column(String(10), nullable=False)
    is_premium = Column(Boolean, default=False)
    date_create = Column(DateTime, default=datetime.now)
    date_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)
