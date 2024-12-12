from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.expiry_time_taken

security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    os.environ['ACCESS_TOKEN'] = encoded_jwt  # Store token in environment
    os.environ['EXPIRED_TOKEN_TIME'] = str(expire.timestamp())  # Store expiry time in environment

    return encoded_jwt

def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token.credentials, credentials_exception)

def verify_access_token(token: str, credentials_exception):
    stored_token = os.getenv('ACCESS_TOKEN')
    stored_expiry = os.getenv('EXPIRED_TOKEN_TIME')

    if not stored_token or token != stored_token:
        raise HTTPException(status_code=403, detail="Token mismatch or missing")

    if stored_expiry and datetime.utcnow().timestamp() > float(stored_expiry):
        raise HTTPException(status_code=401, detail="Token expired")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception