from fastapi import FastAPI

from .routers import develop, network#, set_configs#, sim
from .controllers import * 

app = FastAPI()

# app.include_router(sim.router)
app.include_router(network.router)
app.include_router(develop.router)
# app.include_router(set_configs.router)



@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    config ={}
    app.run(host="0.0.0.0.0", port=8000, debug=True)