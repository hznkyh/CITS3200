import logging
from threading import Lock, Thread
import sys
import os
from pathlib import Path
import json

import copy
from venv import logger
from mtdgui.controllers.loggerConfig import setup_logger
# Get the absolute path of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the "s" directory
s_directory = os.path.join(current_script_dir, "..", "simulator")
sys.path.append(s_directory)

from adapter import *

import simpy
env = simpy.Environment()
simulation_thread = None
simulation_speed = 1.0
stored_params = None

import logging
logger = logging.getLogger()


setup_logger(logger)

# Create a shared list using Manager
message_queue = [] # This will hold our messages from the simulation
message_queue_lock = Lock() 

# This callback will append simulation data to our message queue
def sse_callback(ad,**kwarg):
    '''The function `sse_callback` adds a notification message to a message queue based on the name, type,
    and wait time provided.
    
    Parameters
    ----------
    name : str
        The name parameter is a string that represents the name of the notification or event. It is used to
    identify the specific notification or event that is being processed.
    typeof : str
        The `typeof` parameter is a string that indicates the type of event or action that occurred. It can
    have two possible values: "Wait Finished" or any other value.
    wait : float
        The `wait` parameter represents the amount of time (in time units) that the `name` has waited
    before the callback is triggered.
    
    '''


    with message_queue_lock:
        message_queue.append(copy.deepcopy(kwarg.get_compromised_users()))
    


    # if(kwarg["typeof"] != "Wait Finished"):

    #     msg= f"Notification: {name} reneged after waiting for {wait:.3f} time units."
    # else :

    #     msg= f"Notification: {name} Wait Finished at {wait:.3f} time units."


parameters = {
    "start_time": 0,
    "finish_time": 10000,
    "checkpoints": range(0, 10000, 1000),
    "new_network": True,
    "scheme": 'random',
    "mtd_interval": None,
    "custom_strategies": None,
    "total_nodes": 100,
    "total_endpoints": 5,
    "total_subnets": 8,
    "total_layers": 4,
    "target_layer": 4,
    "total_database": 2,
    "terminate_compromise_ratio": 0.8,
    "callback": sse_callback
}



res= []
logger.info("Starting the application")
final_params = {'env':env,'res':res} | parameters 
# final_params = {'res':res} | parameters 
if stored_params is not None:
    final_params = final_params | stored_params 
try: 
    simulation_thread = Thread(target=create_sim_test, kwargs=final_params)
    simulation_thread.start()
    simulation_thread.join()

    # graph_data =  {index: serialize_graph(data) for index, data in enumerate(res)}
except: 


    # uvicorn.run(app,host="0.0.0.0", port=8000)

