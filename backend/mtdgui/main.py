from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union, Optional, Dict, Any
import uvicorn

from routers import develop, network,config#, set_configs#, sim
from controllers import * 

app = FastAPI()

app.include_router(config.router)
app.include_router(network.router)
app.include_router(develop.router)
# app.include_router(set_configs.router)



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


# if __name__ == "__main__":
#     config ={}
#     app.run(host="0.0.0.0", port=8000, debug=True)
#     # uvicorn.run(app,host="0.0.0.0", port=8000)




class Item(BaseModel):
    name: str
    age: int
    is_TrueMan: Union[bool, None]=None

@app.post("/update_item/")
def update_item(item: Item):
    item.age += 10
    print(item)
    return {'item':item}

class MTD_PRIORITYItem(BaseModel):
    CompleteTopologyShuffle: Union[int, None]
    HostTopologyShuffle: Union[int, None]
    IPShuffle: Union[int, None]
    OSDiveristy: Union[int, None]
    PortShuffle: Union[int, None]
    ServiceDiversity: Union[int, None]
    UserShuffle: Union[int, None]

class formData(BaseModel):
    total_nodes: int
    total_endpoints: int
    total_layers: int
    terminate_compromise_ratio: float
    scheme: str
    mtd_interval: float
    MTD_PRIORITY: Any = None

@app.post("/update_submit/")
def update_item(item: formData):
    form_data_values = {
        "total_nodes": item.total_nodes,
        "total_endpoints": item.total_endpoints,
        "total_layers": item.total_layers,
        "terminate_compromise_ratio": item.terminate_compromise_ratio,
        "scheme": item.scheme,
        "mtd_interval": item.mtd_interval,
    }
    
    mtd_priority_values = item.MTD_PRIORITY
    if mtd_priority_values is None:
        mtd_priority_values = {}

    mtd_priority = {'MTD_PRIORITY': mtd_priority_values}
    print(form_data_values)
    
    print(mtd_priority)
    return {
        'form_data': form_data_values, **mtd_priority
    }



