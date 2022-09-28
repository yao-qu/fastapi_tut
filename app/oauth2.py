from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')
# SECRET KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire_time})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_access_token(token:str, credentials_exception):
    try:
        payLoad = jwt.decode(token, SECRET_KEY)
        id:str = payLoad.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = 401, detail=f"Could not validation credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
