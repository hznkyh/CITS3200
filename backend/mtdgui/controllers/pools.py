import itertools
import logging
import time
from typing import Annotated, List
from auth import get_current_active_user
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from concurrent.futures import Future
from concurrent.futures import ProcessPoolExecutor,as_completed
from threading import Lock, Thread
from controllers import serialize_graph, ProcessPoo
from simulator.adapter import create_sim
from simulator import create_sim, configs
import simpy
from models import User, ParameterRequest, Parameters
from sessions import sessions
from config import parameters
import copy
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

def handleRequest(req : ParameterRequest): 
    cur_config = req.config
    cur_run = req.run
    run_dict = cur_run.model_dump() 
    stored_params = {key: value for key, value in run_dict.items() if value is not None}
    #Handle config_variables
    if (cur_config is not None): 
        config_params = config_params.model_dump()
    configs.config = configs.set_config(config_params) 
    env = simpy.Environment()    
    print('init',env)
    final_params = {'env':env} | parameters 
    print("INITIAL PARAMS", final_params)
    print("STORED PARAMS",stored_params)
    if stored_params is not None:
        final_params = final_params | stored_params 
    print("FINAL PARAMS", final_params)
    if type(final_params["checkpoints"]) is int: 
        final_params["checkpoints"] =  range(final_params["start_time"], int(final_params["finish_time"]), final_params["checkpoints"])
    return req.graph , create_sim(final_params)
