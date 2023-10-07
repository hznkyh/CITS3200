from datetime import datetime, timedelta
from typing import Annotated, Union
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from models.token import *
from models.User import *
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from config import settings
from sessions import sessions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db, client_uuid: str):
    if client_uuid in db:
        user_dict = db[client_uuid]
        return User(**user_dict)
    else:
        db[client_uuid] = { "uuid" : client_uuid}
        user_dict = db[client_uuid]
        return User(uuid=client_uuid)


def verify_session(sessions,client_uuid):
    return get_user(sessions, client_uuid)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    global sessions
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(sessions, client_uuid=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):  
    if current_user == None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
