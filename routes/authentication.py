from email_validator import validate_email
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from models.user import User
from schemas.user import UserSchem
from utils.jwt_handler import create_access_token

auth_router = APIRouter()


@auth_router.post('/register')
async def register(user: UserSchem, session: AsyncSession = Depends(get_db)) -> dict:
    try:
        email = validate_email(user.email).email
    except Exception as e:
        raise HTTPException(status_code=400, detail="Неверно указанный email")
    user_for_db = User(email=email, password=user.password)
    session.add(user_for_db)
    await session.commit()
    await session.refresh(user_for_db)
    token = create_access_token(email)
    return {
        "token": token
    }


@auth_router.post('/login')
async def login(user: UserSchem, session: AsyncSession = Depends(get_db)) -> dict:
    user_ex = await session.execute(select(User).where(User.email == user.email))
    res_ex = user_ex.scalars().first()
    if not res_ex:
        raise HTTPException(status_code=404)
    if not res_ex.check_password(user.password):
        raise HTTPException(status_code=400)
    token = create_access_token(user.email)
    return {
        "token": token
    }