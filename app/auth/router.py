from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.schemas import InitData
from auth.models import User
from auth.auth import create_jwt
from database.database import get_db

router = APIRouter()


def authenticate_user(init_data: InitData, db: Session):
    user = db.query(User).filter(User.tg_id == init_data.tg_id).first()
    if user:
        user.first_name = init_data.first_name
        user.last_name = init_data.last_name
        user.username = init_data.username
        user.language_code = init_data.language_code
        user.is_premium = init_data.is_premium
        db.commit()
        db.refresh(user)
    else:
        user = User(
            tg_id=init_data.tg_id,
            first_name=init_data.first_name,
            last_name=init_data.last_name,
            username=init_data.username,
            language_code=init_data.language_code,
            is_premium=init_data.is_premium
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@router.post("/access")
def get_access_token(init_data: InitData, db: Session = Depends(get_db)):
    user = authenticate_user(init_data, db)
    token = create_jwt({"user_id": user.tg_id}, lifetime_seconds=3600)
    return {"access_token": token}
