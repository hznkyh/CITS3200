"""
This module contains functions for user authentication and session management.

Functions
---------
get_user(db, client_uuid)
    Retrieve a user from the database, or create a new user if one does not exist.
verify_session(sessions, client_uuid)
    Verify if a session is valid for a given client UUID.
create_access_token(data, expires_delta=None)
    Create an access token for a user.
get_current_user(token)
    Get the current user from a JWT token.
get_current_active_user(current_user)
    Get the current active user.
"""
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
    """
    Retrieve a user from the database, or create a new user if one does not exist.

    Parameters
    ----------
    db : dict
        A dictionary representing the database of users.
    client_uuid : str
        A string representing the UUID of the client.

    Returns
    -------
    User
        A User object representing the retrieved or created user.
    """
    if client_uuid in db:
        user_dict = db[client_uuid]
        return User(**user_dict)
    else:
        db[client_uuid] = {"uuid": client_uuid}
        user_dict = db[client_uuid]
        return User(uuid=client_uuid)

def verify_session(sessions, client_uuid):
    """
    Verify if a session is valid for a given client UUID.

    Args:
        sessions (list): A list of session objects.
        client_uuid (str): The UUID of the client.

    Returns:
        dict: A dictionary containing the user information if the session is valid,
        otherwise None.
    """
    return get_user(sessions, client_uuid)

def verify_session(sessions, client_uuid):
    return get_user(sessions, client_uuid)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Create an access token for a user.

    Parameters
    ----------
    data : dict
        The data to be encoded in the token.
    expires_delta : Union[timedelta, None], optional
        The time delta for the token to expire, by default None.

    Returns
    -------
    bytes
        The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Get the current user from a JWT token.

    Parameters
    ----------
    token : str
        The JWT token to decode.

    Returns
    -------
    dict
        A dictionary containing information about the user.

    Raises
    ------
    HTTPException
        If the credentials could not be validated.
    """
    global sessions
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
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
    """
    Get the current active user.

    Parameters
    ----------
    current_user : User
        The current user.

    Raises
    ------
    HTTPException
        If the user is inactive.

    Returns
    -------
    User
        The current active user.
    """
    if current_user == None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
