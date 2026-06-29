from utils.db import db
from utils.security import hash_password

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
