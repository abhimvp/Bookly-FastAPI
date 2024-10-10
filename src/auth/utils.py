# define alogorithems we are going to use to hash our password
from datetime import timedelta,datetime
from passlib.context import CryptContext
import jwt
from src.config import Config
import uuid
import logging

passwd_context = CryptContext(schemes=["bcrypt"])

#seconds
ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    hash= passwd_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

# encode our token
from datetime import timedelta, datetime

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}
    payload['user'] = user_data
    expiry_time = datetime.utcnow() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['exp'] = expiry_time.timestamp()  # Convert to Unix timestamp
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token

# decode the token
def decode_token(token: str):
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.pyJWTError as e:
        logging.exception(e)
        return None