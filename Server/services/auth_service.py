from utils.db import db
from utils.security import hash_password
import bcrypt


async def authenticate_user(email: str, password: str):
    user = await db.user.find_unique(where={"email": email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    return None


def create_user(username , email , password , role , embedding_list):
    try:
        user = db.User.create({
            'username': username,
            'email': email,
            'password': hash_password(password),
            'role': role,
            'face_embedding': embedding_list
        })

        return user
    except:
        return "Error occured while creating user"
