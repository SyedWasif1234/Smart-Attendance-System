import jwt
from datetime import datetime, timedelta, timezone
import bcrypt
import os

from utils.db import db

SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGO = os.getenv("ALGORITHM")


def hash_password(password:str)->str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_AccessToken(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire , "type": "access"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)

    return encoded_jwt


def create_RefreshToken(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode = {**data, "exp": expire, "type": "refresh"}
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGO)


def verify_token(token: str, is_refresh=False):
    secret = REFRESH_SECRET_KEY if is_refresh else SECRET_KEY
    try:
        return jwt.decode(token, secret, algorithms=[ALGO])
    except jwt.PyJWTError:
        return None


async def update_refresh_token(user_id: str, refresh_token: str):
    expiry = datetime.now(timezone.utc) + timedelta(days=7)
    await db.user.update(
        where={"id": user_id},
        data={"refreshToken": refresh_token, "refreshTokenExpiry": expiry}
    )

async def clear_refresh_token(user_id: str):
    await db.user.update(
        where={"id": user_id},
        data={"refreshToken": None, "refreshTokenExpiry": None}
    )