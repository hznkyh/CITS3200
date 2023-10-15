import logging
from simulator.adapter import create_sim
from simulator import create_sim, configs
from models import ParameterRequest
from config import parameters


def handleRequest(graph_name, request: ParameterRequest):
    req = request.model_dump()
    stored_params = {
        key: value for key, value in req["run"].items() if value is not None
    }
    # Handle config_variables
    if req.get("config") is not None:
        config_params = {
            key: value for key, value in req["config"].items() if value is not None
        }
        configs.config = configs.set_config(config_params)
    final_params = parameters
    if stored_params is not None:
        final_params = final_params | stored_params
    if type(final_params["checkpoints"]) is int:
        final_params["checkpoints"] = range(
            final_params["start_time"],
            int(final_params["finish_time"]),
            final_params["checkpoints"],
        )
    return graph_name, create_sim(**final_params)
