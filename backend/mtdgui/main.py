from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union, Optional

from routers import develop, network#, sim
from controllers import * 

app = FastAPI()

# app.include_router(sim.router)
app.include_router(network.router)
app.include_router(develop.router)



app.add_middleware(
    CORSMiddleware,    
    allow_origins= "http://localhost:5173",    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

class Item(BaseModel):
    name: str
    age: float
    is_TrueMan: Union[bool, None]=None

@app.post("/update_item/")
def update_item(item: Item):
    item.age += 10
    print(item)
    return {'item':item}

class MTD_PRIORITYItem(BaseModel):
    CompleteTopologyShuffle: Optional[float]
    HostTopologyShuffle: Optional[float]
    IPShuffle: Optional[float]
    OSDiveristy: Optional[float]
    PortShuffle: Optional[float]
    ServiceDiversity: Optional[float]
    UserShuffle: Optional[float]

class formData(BaseModel):
    total_nodes: float
    total_endpoints: float
    total_layers: float
    terminate_compromise_ratio: float
    scheme: str
    mtd_interval: float
    MTD_PRIORITY: Union[MTD_PRIORITYItem, None]

@app.post("/update_submit/")
def update_item(item: formData):
    if item.MTD_PRIORITY is None:
        pass
    print(item)
    return {'item': item.dict()}

