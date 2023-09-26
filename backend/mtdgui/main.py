from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Optional, Dict, Any
from jose import jwt, JWTError
import datetime
import uvicorn
import os
import pathlib
from controllers.loggerConfig import setup_logger
import uuid
from routers import (
    develop,
    network,
    config,
    webSocket,
    webSocketDev,
    streaming,
)  # , set_configs#, sim
from controllers import *

import logging

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

app = FastAPI(debug=True)

app.include_router(config.router)
app.include_router(network.router)
app.include_router(develop.router)
app.include_router(streaming.router)
app.include_router(webSocket.router)
app.include_router(webSocketDev.router)


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


def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/generate-token/")
async def generate_token():
    session_data = {"session": str(uuid.uuid4()) }
    token = create_jwt_token(session_data)
    return {"access_token": token}

@app.middleware("http")
async def decode_jwt(request: Request, call_next):
    print("Request:", request.headers)
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        print("Received token:", token)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print("Decoded payload:", payload)
            request.state.session_data = payload
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            raise HTTPException(status_code=401, detail="Invalid token")
    response = await call_next(request)
    return response

@app.get("/test-token/")
async def test_token(request: Request):
    session_data = request.state.session_data if hasattr(request.state, 'session_data') else None
    return {"session_data": session_data}


if __name__ == "__main__":
    log_file = pathlib.Path('Logs/debug.log')

    if not log_file.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
    logger = logging.getLogger()
    setup_logger(logger)
    
    uvicorn.run("main:app",host="0.0.0.0", port=8000, reload=True)
