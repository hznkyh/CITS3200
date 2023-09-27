import json
import logging
import threading
import networkx as nx
from models.forms import ParameterRequest
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, HTTPException
from itertools import chain, count
import simpy
from controllers.serialiser import serialize_graph
import sys
import os
from pathlib import Path
from simulator.adapter import create_sim
from typing import Optional, Union, List

from concurrent.futures import Future, ProcessPoolExecutor
logger = logging.getLogger(__name__)
POOL = ProcessPoolExecutor(max_workers=1)  # or any other number
future: Union[Future, None ]  = None

router = APIRouter(prefix="/network",
                   tags=["network"], responses={404: {"description": "Not found"}})

stored_params = None
parameters = {
    "start_time": 0,
    "finish_time": 3000,
    "checkpoints": range(0, 3000, 1000),
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
    global stored_params
    
    if not stored_params is None :
        final_params = parameters | stored_params
    else :
        final_params = parameters
        
    logger.debug("FINAL PARAMS", final_params)
    
    if "checkpoints" in final_params:
        if type(final_params["checkpoints"]) is int:
            final_params["checkpoints"] = range(final_params["start_time"], int(final_params["finish_time"]), final_params["checkpoints"])

    future = POOL.submit(create_sim, **final_params)  # Using the global POOL from workers.py
    POOL.shutdown(wait=True)
    try:
        result = future.result()
        graph_data = {index: serialize_graph(data) for index, data in enumerate(result['snapshots'])}
    except Exception as e:
        logger.error(f"Error in simulation execution. Reason: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error in simulation execution. Reason: {e}"
        )
        #Todo add below if possible, then remove from tests 
        # finally: 
        #     if stored_params is not None: 
        #         stored_params = None
    return JSONResponse(content=graph_data)

@router.get("/graph-old")
async def get_graph():
    '''The function `get_graph()` starts a simulation thread and returns the results in a serialized graph
    format. Global threads and envs are used to ensure that in error, the threads are easily terminated. 
    
    Returns
    -------
        The code returns a JSON response containing graph data.
    
    '''
    global simulation_thread, stored_params
    if simulation_thread is not None:
        simulation_thread.join()
        raise HTTPException(
            status_code=400, detail="Simulation already running")
    
    # final_params = {'env':env,'res':res} | parameters 
    
    # print("INITIAL PARAMS", final_params)
    # print("STORED PARAMS",stored_params)
    
    # if stored_params is not None: 
    final_params = parameters | stored_params if not stored_params is None else {}
        
    print("FINAL PARAMS", final_params)
    if type(final_params["checkpoints"]) is int: 
        final_params["checkpoints"] =  range(final_params["start_time"], int(final_params["finish_time"]), final_params["checkpoints"])
    try: 
        simulation_thread = threading.Thread(target=create_sim, kwargs=final_params)
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
    global future
    if future is None:
        logger.debug("No simulation running and is alive")
        raise HTTPException(status_code=200, detail=f"No simulation running")
    elif future.running():
        logger.debug("Simulation is running and is alive")
        future.cancel()
        logger.debug("Simulation stopped")
        raise HTTPException(status_code=200, detail=f"Simulation stopped")
    POOL.shutdown(wait=True)
    return JSONResponse(content="Simulation stopped", status_code=200)
    
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
