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
    CompleteTopologyShuffle: Union[float, None]
    HostTopologyShuffle: Union[float, None]
    IPShuffle: Union[float, None]
    OSDiveristy: Union[float, None]
    PortShuffle: Union[float, None]
    ServiceDiversity: Union[float, None]
    UserShuffle: Union[float, None]

@app.post("/update_MTDPsubmit/")
def update_item(item: MTD_PRIORITYItem):
    print(item.model_dump_json())
    return {'item': item.model_dump_json()}
    #return {'item': item.dict()}

class formData(BaseModel):
    total_nodes: float
    total_endpoints: float
    total_layers: float
    terminate_compromise_ratio: float
    scheme: str
    mtd_interval: float

@app.post("/update_submit/")
def update_item(item: formData):
    print(item.model_dump_json())
    return {'item': item.model_dump_json()}
    #return {'item': item.dict()}



