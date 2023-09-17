import json
import threading
import networkx as nx
from models.forms import Item,MTD_PRIORITYItem,formData,formDataAdv
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, HTTPException
from itertools import chain, count
# from networkx.utils import to_tuple
import simpy
from controllers.serialiser import serialize_graph
import sys
import os
from pathlib import Path
# Construct the path to the "s" directory
s_directory = os.path.join(Path(__file__).parents[3], "simulator")
# Add the "s" directory to the Python path
sys.path.append(s_directory)
n_directory = os.path.join(Path(__file__).parents[2])
# Add the "s" directory to the Python path
sys.path.append(n_directory)
# from run import get_sim_json
from adapter import *
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
    "total_nodes": 20,
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
    

@router.post("/update_submit/")
def update_item(item: formData, itemAdv: formDataAdv):
    global stored_params
    form_data_values = {
        "total_nodes": item.total_nodes,
        "total_endpoints": item.total_endpoints,
        "total_layers": item.total_layers,
        "terminate_compromise_ratio": item.terminate_compromise_ratio,
        "scheme": item.scheme,
        "mtd_interval": item.mtd_interval,
        "finish_time": item.finish_time,
        "checkpoints": item.checkpoints,
        "total_subnets": item.total_subnets,
        "target_layer": item.target_layers,
    }
    
    mtd_priority_values = itemAdv.MTD_PRIORITY
    if mtd_priority_values is None:
        mtd_priority_values = {}
    mtd_priority = {'MTD_PRIORITY': mtd_priority_values}

    mtd_trigger_values = itemAdv.MTD_TRIGGER_INTERVAL
    if mtd_trigger_values is None:
        mtd_trigger_values = {}
    mtd_trigger = {'MTD_TRIGGER_INTERVAL': mtd_trigger_values}

    print(form_data_values)
    print(mtd_priority)
    print(mtd_trigger)
    # return RedirectResponse("https://localhost:8000/network/graph")
    print("Setting stored params to: ",stored_params)
    filtered_dict = {key: value for key, value in form_data_values.items() if value is not None}
    stored_params = filtered_dict
    return {
        'form_data': form_data_values, **mtd_priority, **mtd_trigger
    }



# { 
#     run.py { 
#         total_nodes
#     }
#     constants.py { 
#         optional
#     }
# }
