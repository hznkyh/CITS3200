"""
This module contains the main FastAPI application for the backend of the project.
It includes routers for network, webSocket, streaming, statistics, and graph configuration.
It also includes controllers for setting up logger and process pool.
The app has endpoints for authentication, token generation, and testing.
"""
import logging
from datetime import timedelta
from typing import Annotated
from uuid import uuid4

import uvicorn
from auth import create_access_token, get_current_active_user, verify_session
from config import settings
from controllers import ProcessPoo
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from logging.handlers import RotatingFileHandler
from models import Token, User
from routers import network, multiSim, statistics
from sessions import sessions



# logger = logging.getLogger('mtdgui.main')  # Convention: <app_name>.<module_name>
# logger.debug("Debug message from main.py")

logger = logging.getLogger(__name__)
logger.info("init main")

app = FastAPI(debug=True)
app.include_router(network.router)
app.include_router(statistics.router)
app.include_router(multiSim.router)
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
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>FASTAPI Documentation</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body>
            <div class="container mt-5">
                <h1>Welcome to the FASTAPI Application</h1>
                <p>This is a brief guide on how to use the API and access its documentation.</p>
                
                <h2>Authentication</h2>
                <p>To authenticate, make a POST request to <code>/token</code> with your username and password:</p>
                <pre><code>
                POST /token
                {
                "username": "your_username",
                "password": "your_password"
                }
                </code></pre>
                <p>You'll receive a JWT token in response. Include this token in the Authorization header of your subsequent requests:</p>
                <pre><code>
                Authorization: Bearer YOUR_TOKEN_HERE
                </code></pre>
                
                <h2>Accessing the Documentation</h2>
                <p>FASTAPI provides an interactive API documentation. You can access it by navigating to:</p>
                <a href="/docs" target="_blank">/docs</a>
                <p>This will provide you with a list of all available endpoints, their parameters, and expected responses.</p>
                
                <h2>Further Information</h2>
                <p>If you have more questions, please contact the administrator or refer to the official FASTAPI documentation.</p>
            </div>

            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
            </body>
            </html>
    """,
        status_code=status.HTTP_200_OK,
    )


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

#   TODO: Implement this for singleton pattern for process pool
# @app.on_event("shutdown")
# def shutdown_event():
#     # Shutdown the pool when the app stops
#     ProcessPoo.shutdown()

#   ! DO NOT RUN THIS IN PRODUCTION
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)