import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import jwt, JWTError

from config import Config


def create_access_token(email: str) -> str:
    payload = {"email": email, "expires": time.time() + 3600}
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token


def create_refresh_token(email: str) -> str:
    payload = {
        "email": email,
        "expires": time.time() + 1209600,  # 14 days
    }
    token = jwt.encode(payload, Config.REFRESH_SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str) -> int:
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )

        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token expired!"
            )

        return data["email"]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )


def verify_refresh_token(token: str) -> dict:
    try:
        data = jwt.decode(token, Config.REFRESH_SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No refresh token supplied",
            )

        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token expired!"
            )

        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
        )
