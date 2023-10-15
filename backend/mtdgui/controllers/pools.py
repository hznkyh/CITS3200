
from simulator.adapter import create_sim
from simulator import create_sim, configs
import simpy
from models import ParameterRequest
from config import parameters
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

def handleRequest(graph_name, request : ParameterRequest): 
    """
    Handles the execution of a single simulation. Sets the parameters, 
    runs the simulation and returns the necessary results

    Parameters
    ----------
    graph_name : str
       String representing the name of the graph

    
    request : ParameterRequest
       The request containing the parameters and configuration
    
    Returns
    -------
    graph_name : str
       String representing the name of the graph

    create_sim(**final_params): dict
        Returns an dictionary containing the keys snapshots and evaluation.
        Includes all information necessary to render the information on the 
        frontend.  

    """
    req = request.model_dump()
    stored_params = {key: value for key, value in req['run'].items() if value is not None}
    #Handle config_variables
    if (req.get('config') is not None): 
        config_params =  {key: value for key, value in req['config'].items() if value is not None}

        configs.config = configs.set_config(config_params) 
    final_params = parameters 
    if stored_params is not None:
        final_params = final_params | stored_params 
    if type(final_params["checkpoints"]) is int: 
        final_params["checkpoints"] =  range(final_params["start_time"], int(final_params["finish_time"]), final_params["checkpoints"])
    return graph_name , create_sim(**final_params)
