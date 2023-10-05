from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from controllers.loggerConfig import setup_logger

from routers import network,config, webSocket ,webSocketDev, streaming, statistics #, set_configs#, sim
from controllers import * 

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
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import Token, User
from routers import (network, graphConfig, # , set_configs#, sim 
                     streaming, webSocket, multiSim)
from sessions import sessions

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
# Initialize the pool when the app starts
pool = ProcessPoo().get_pool()

app = FastAPI(debug=True)

app.include_router(graphConfig.router)
app.include_router(network.router)
app.include_router(statistics.router)
app.include_router(streaming.router)
app.include_router(webSocket.router)
app.include_router(multiSim.router)


# app.include_router(set_configs.router)


app.add_middleware(
    CORSMiddleware,    
    allow_origins= "http://localhost:8080/",    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

@app.get("/uuid")
async def uuid():
    return JSONResponse(content=str(uuid4()), status_code=status.HTTP_200_OK)


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = verify_session(sessions=sessions, client_uuid=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.uuid}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/test-token/", response_model=User)
async def test_token(client: Annotated[User, Depends(get_current_active_user)]):
    return JSONResponse(content=client.uuid, status_code=status.HTTP_200_OK)

@app.get("/sessions/")
async def all_sessions():
    return JSONResponse(content=sessions, status_code=status.HTTP_200_OK)

@app.on_event("shutdown")
def shutdown_event():
    # Shutdown the pool when the app stops
    ProcessPoo.shutdown()


if __name__ == "__main__":
    log_file = pathlib.Path('Logs/debug.log')

    if not log_file.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
    logger = logging.getLogger()
    setup_logger(logger)
    
    uvicorn.run("main:app",host="0.0.0.0", port=8000, reload=True)
