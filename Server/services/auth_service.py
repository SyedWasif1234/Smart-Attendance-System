from utils.db import db
from utils.security import hash_password
from fastapi import HTTPException, status
import bcrypt


async def authenticate_user(email: str, password: str):
    user = await db.user.find_unique(where={"email": email})
    if user and user.password and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    return None


async def create_user(username: str, email: str, password: str, embedding_list: list):
    try:
        # Check for duplicate email before creating
        existing_user = await db.user.find_unique(where={"email": email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )

        user = await db.user.create(
            data={
                'username': username,
                'email': email,
                'password': hash_password(password),
                'face_embedding': embedding_list
            }
        )

        return user
    except HTTPException:
        raise  # Forward HTTP errors directly
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while creating user: {str(e)}"
        )
