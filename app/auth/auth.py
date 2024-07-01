import jwt
import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from aiogram.utils.web_app import check_webapp_signature
from auth.models import User
from settings import settings
from database.database import get_db
from auth.schemas import UserBase as UserSchema
from datetime import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt(data: dict, lifetime_seconds: int):
    payload = data.copy()
    payload['exp'] = int(time.time()) + lifetime_seconds
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def authenticate_user(init_data: dict, db: Session):
    if not check_webapp_signature(settings.TELEGRAM_BOT_TOKEN, init_data):
        raise HTTPException(status_code=403, detail="Invalid signature")

    user_data = init_data['user']
    tg_id = user_data['id']
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if user:
        user.username = user_data.get('username')
        user.first_name = user_data.get('first_name')
        user.last_name = user_data.get('last_name')
        user.language_code = user_data.get('language_code')
        user.date_update = datetime.now()
    else:
        user = User(
            tg_id=tg_id,
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            language_code=user_data.get('language_code'),
            date_create=datetime.now(),
            date_update=datetime.now()
        )
        db.add(user)
    db.commit()
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    user = db.query(User).filter(User.tg_id == user_id).first()
    if user is None:
        raise credentials_exception
    return UserSchema.from_orm(user)

