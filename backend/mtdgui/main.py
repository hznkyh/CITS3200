from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union, Optional, Dict, Any
import uvicorn
from controllers.loggerConfig import setup_logger

from routers import develop, network,config, webSocket ,webSocketDev, streaming #, set_configs#, sim
from controllers import * 

import logging
logger = logging.getLogger()


setup_logger(logger)


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


# if __name__ == "__main__":
#     config ={}
#     app.run(host="0.0.0.0", port=8000, debug=True)
    # uvicorn.run(app,host="0.0.0.0", port=8000)

