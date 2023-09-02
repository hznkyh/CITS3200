from fastapi import FastAPI

from routers import develop, network#, sim
from controllers import * 

app = FastAPI()

# app.include_router(sim.router)
app.include_router(network.router)
app.include_router(develop.router)



@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}