"""
This module contains the main FastAPI application for the backend of the project.
It includes routers for network, webSocket, streaming, statistics, and graph configuration.
It also includes controllers for setting up logger and process pool.
The app has endpoints for authentication, token generation, and testing.
"""
import logging
import pathlib
from datetime import timedelta
from typing import Annotated
from uuid import uuid4

import uvicorn
from auth import create_access_token, get_current_active_user, verify_session
from config import settings
from controllers import setup_logger, ProcessPoo
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import Token, User
from routers import network, multiSim, statistics
from sessions import sessions

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
# Initialize the pool when the app starts
pool = ProcessPoo().get_pool()

app = FastAPI(debug=True)

app.include_router(network.router)
app.include_router(statistics.router)
app.include_router(multiSim.router)


# app.include_router(set_configs.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:8080/",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return HTMLResponse(
        content="""
        <html>
            <head>
                <title>Hello Bigger Applications!</title>
            </head>
            <body>
                <h1>Hello Bigger Applications!</h1>
                <p>Welcome to my API.</p>
            </body>
        </html>
    """,
        status_code=status.HTTP_200_OK,
    )


{"message": "Hello Bigger Applications!"}


@app.get("/uuid")
async def uuid():
    return JSONResponse(content=str(uuid4()), status_code=status.HTTP_200_OK)


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Authenticate user and return an access token.

    Parameters
    ----------
    form_data : OAuth2PasswordRequestForm
        The form data containing the user's credentials.

    Returns
    -------
    Token
        An access token and its type.

    Raises
    ------
    HTTPException
        If the user's credentials are incorrect.
    """
    user = verify_session(sessions=sessions, client_uuid=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.uuid}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/test-token/", response_model=User)
async def test_token(client: Annotated[User, Depends(get_current_active_user)]):
    """
    Test the authentication token of the user.

    Parameters
    ----------
    client : User
        The authenticated user.

    Returns
    -------
    JSONResponse
        The UUID of the authenticated user.

    Raises
    ------
    HTTPException
        If the user is not authenticated.
    """
    return JSONResponse(content=client.uuid, status_code=status.HTTP_200_OK)


#   TODO: Remove this endpoint
# @app.get("/sessions/")
# async def all_sessions():
#     return JSONResponse(content=sessions, status_code=status.HTTP_200_OK)

#   TODO: Implement this for singleton pattern for process pool
# @app.on_event("shutdown")
# def shutdown_event():
#     # Shutdown the pool when the app stops
#     ProcessPoo.shutdown()


if __name__ == "__main__":
    log_file = pathlib.Path("Logs/debug.log")

    if not log_file.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    setup_logger(logger)

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
