import jwt
from datetime import datetime, timedelta, timezone
import bcrypt

def hash_password(password:str)->str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_AccessToken():


def create_RefreshToken():


def varify_Token():


def update_RefreshToken():


def clear_RefreshToken():