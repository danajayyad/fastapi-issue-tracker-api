# Password hashing (CryptContext) & JWT generation functions
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from .config import settings
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password :str):
    return bcrypt_context.hash(password)

def verify_password(password:str, hashed_password:str):
    return bcrypt_context.verify(password, hashed_password)


def create_access_token(token_data: dict):
    expires_delta = timedelta(minutes=settings.ACCESS_TOEKN_EXPIRY_MINUTES)
    to_encode = token_data.copy()
    expires = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp' : expires})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)