import json
import threading
import networkx as nx
# from models.forms import Item,MTD_PRIORITYItem,formData
from models.forms import ParameterRequest
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, HTTPException
from itertools import chain, count
# from networkx.utils import to_tuple
import simpy
from controllers.serialiser import serialize_graph
import sys
import os
from pathlib import Path
from simulator.adapter import * 
# Construct the path to the "s" directory
# s_directory = os.path.join(Path(__file__).parents[3], "simulator")
# # Add the "s" directory to the Python path
# sys.path.append(s_directory)
# n_directory = os.path.join(Path(__file__).parents[2])
# # Add the "s" directory to the Python path
# sys.path.append(n_directory)
# # from run import get_sim_json
# from adapter import *
#
# from adapter import sim_params, run_sim

router = APIRouter(prefix="/network",
                   tags=["network"], responses={404: {"description": "Not found"}})

# env = simpy.Environment()
env = simpy.Environment()
simulation_thread = None
simulation_speed = 1.0
stored_params = None
parameters = {
    "start_time": 0,
    "finish_time": 10000,
    "checkpoints": range(0, 10000, 1000),
    "new_network": True,
    "scheme": 'random',
    "mtd_interval": None,
    "custom_strategies": None,
    "total_nodes": 50,
    "total_endpoints": 5,
    "total_subnets": 8,
    "total_layers": 4,
    "target_layer": 4,
    "total_database": 2,
    "terminate_compromise_ratio": 0.8
}

@router.get("/")
async def read_items():
    return "Hello World"

@router.get("/graph")
async def get_graph():
    '''The function `get_graph()` starts a simulation thread and returns the results in a serialized graph
    format. Global threads and envs are used to ensure that in error, the threads are easily terminated. 
    
    Returns
    -------
        The code returns a JSON response containing graph data.
    
    '''
    global simulation_thread, env, stored_params
    # configs.config = 0
    # set_config()
    # print(configs.config)
    res = []
    print("thread", simulation_thread)
    if simulation_thread is not None:
        simulation_thread.join()
        raise HTTPException(
            status_code=400, detail="Simulation already running")
    
    print('init',env)
    res= []
    final_params = {'env':env,'res':res} | parameters 
    print("INITIAL PARAMS", final_params)
    print("STORED PARAMS",stored_params)
    if stored_params is not None:
        final_params = final_params | stored_params 
    print("FINAL PARAMS", final_params)
    if type(final_params["checkpoints"]) is int: 
        final_params["checkpoints"] =  range(final_params["start_time"], int(final_params["finish_time"]), final_params["checkpoints"])
    try: 
        simulation_thread = threading.Thread(target=create_sim_test, kwargs=final_params)
        simulation_thread.start()
        simulation_thread.join()
        simulation_thread = None
        env = simpy.Environment()
        print("res length", len(res))
        graph_data =  {index: serialize_graph(data) for index, data in enumerate(res)}
    except: 
        raise HTTPException(
            status_code=400, detail="Error in simulation execution."
        ) 
    #Todo add below if possible, then remove from tests 
    # finally: 
    #     if stored_params is not None: 
    #         stored_params = None
    return JSONResponse(content=graph_data)

    
@router.get("/graphDevEnd")
async def stop_graph():
    global simulation_thread, env
    if simulation_thread is None:
        raise HTTPException(status_code=400, detail=f"No simulation running and is alive : {simulation_thread.is_alive()}")
    env.timeout(0)
    simulation_thread.join()
    simulation_thread = None
    env = simpy.Environment()  # create a new environment
    return JSONResponse(content="Simulation stopped", status_code=400)
    
@router.post("/update_all_params")
def update_item(item: ParameterRequest):
    print(item)
    # Handle run parameters
    global stored_params
    run_params = item.run
    run_dict = run_params.model_dump() 
    stored_params = {key: value for key, value in run_dict.items() if value is not None}

    #Handle config_variables
    config_params = item.config
    if (item.config is not None): 
        config_params = config_params.model_dump()
    configs.config = configs.set_config(config_params) 
    return { 
        'item': item
    }

def reset(): 
    global stored_params
    if stored_params is not None: 
        stored_params = None
# { 
#     run.py { 
#         total_nodes
#     }
#     constants.py { 
#         optional
#     }
# }
