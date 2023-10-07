from fastapi import APIRouter
import simpy
from simulator.adapter import *



router = APIRouter(prefix="/config",
                   tags=["config"], responses={404: {"description": "Not found"}})

env = simpy.Environment()
simulation_thread = None
simulation_speed = 1.0

@router.get("/")
async def read_items():
    return "Hello World"

@router.get("/getCurrent")
def getCurrentConfig(): 
    return configs.config

# @router.post("/setCurrent")
# def update_item(item: Item):
#     config=set_config()
#     return {'item':item}

# { 
#     run.py { 
#         total_nodes
#     }
#     constants.py { 
#         optional
#     }
# }