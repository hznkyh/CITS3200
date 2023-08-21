from fastapi import FastAPI

from routers import sim
from controllers import * 

app = FastAPI()

app.include_router(sim.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}