from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    tg_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class InitData(BaseModel):
    tg_id: int
    first_name: str
    last_name: str = None
    username: str = None
    language_code: str
    is_premium: bool
