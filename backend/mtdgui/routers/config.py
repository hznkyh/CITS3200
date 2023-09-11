from model.forms import Item,MTD_PRIORITYItem,formData
from fastapi import APIRouter
from controllers.serialiser import serialize_graph
import simpy
import json
import sys
import os
from pathlib import Path
# Construct the path to the "s" directory
s_directory = os.path.join(Path(__file__).parents[3], "simulator")
sys.path.append(s_directory)
n_directory = os.path.join(Path(__file__).parents[2])
sys.path.append(n_directory)
from adapter import *


router = APIRouter(prefix="/config",
                   tags=["config"], responses={404: {"description": "Not found"}})

# env = simpy.Environment()
env = simpy.Environment()
simulation_thread = None
simulation_speed = 1.0

@router.get("/")
async def read_items():
    return "Hello World"

@router.get("/getCurrent")
def getCurrentConfig(): 
    return config

@router.post("/setCurrent")
def update_item(item: Item):
    config=set_config()
    return {'item':item}

# { 
#     run.py { 
#         total_nodes
#     }
#     constants.py { 
#         optional
#     }
# }