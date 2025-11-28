from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
from .exceptions import TokenExpired, TokenInvalidSignature, TokenInvalidType

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_EXPIRE_MINUTES = 5
REFRESH_EXPIRE_DAYS = 1

def create_access_token(admin_id: int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    payload = {
        "sub" : str(admin_id),
        "type" : "access",
        "exp" : int(expire.timestamp())
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(admin_id: int):
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_EXPIRE_DAYS)
    payload = {
        "sub" : str(admin_id),
        "type" : "refresh",
        "exp" : int(expire.timestamp())
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validate_signature_and_type(client_token: str, token_type: str):
    try:
        payload = jwt.decode(client_token, key=SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
    except JWTError:
        raise TokenInvalidSignature() 

    if payload["type"] != token_type:
        raise TokenInvalidType()
    
    return payload

def validate_access_token(token: str):
    payload = validate_signature_and_type(token, "access")

    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    if exp < datetime.now(timezone.utc):
        raise TokenExpired()
    
    return payload
      

def extract_expire(token: str):
    payload = jwt.decode(token, key=SECRET_KEY, options={"verify_signature": False})
    expires = payload["exp"]
    return  datetime.fromtimestamp(expires, tz=timezone.utc)
    
def extract_admin_id(token: str):
    payload = jwt.decode(token, key=SECRET_KEY, options={"verify_signature": False})
    return payload["sub"]