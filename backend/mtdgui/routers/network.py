import logging
from models.forms import ParameterRequest
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status
from controllers import serialize_graph, ProcessPoo
from simulator import create_sim, configs
from typing import Union
from config import parameters
from concurrent.futures import Future, ProcessPoolExecutor

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/network", tags=["network"], responses={404: {"description": "Not found"}}
)
future: Union[Future, None] = None
stored_params = None



@router.get("/graph")
async def get_graph():
    """The function `get_graph()` starts a simulation thread and returns the results in a serialized graph
    format. Global threads and envs are used to ensure that in error, the threads are easily terminated.

    Returns
    -------
        The code returns a JSON response containing graph data.
    """
    global stored_params

    if not stored_params is None:
        final_params = parameters | stored_params
    else:
        final_params = parameters

    logger.debug("FINAL PARAMS", final_params)

    if "checkpoints" in final_params:
        if type(final_params["checkpoints"]) is int:
            final_params["checkpoints"] = range(
                final_params["start_time"],
                int(final_params["finish_time"]),
                final_params["checkpoints"],
            )
    with ProcessPoolExecutor() as executor:
        future = executor.submit(
            create_sim, **final_params
        )
    # ProcessPoo.shutdown(wait=True)
    try:
        result = future.result()
        graph_data = {
            index: serialize_graph(data)
            for index, data in enumerate(result["snapshots"])
        }
    except Exception as e:
        logger.error(f"Error in simulation execution. Reason: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error in simulation execution. Reason: {e}"
        )
        # Todo add below if possible, then remove from tests
        # finally:
        #     if stored_params is not None:
        #         stored_params = None
    return JSONResponse(content=graph_data, status_code=status.HTTP_200_OK)


@router.get("/graphDevEnd")
async def stop_graph():
    """
    Stop the simulation if it is running.

    Returns:
    --------
    JSONResponse:
        A JSON response indicating that the simulation has been stopped.
    Raises:
    -------
    HTTPException:
        If there is no simulation running, a HTTPException with status code 200 and detail "No simulation running" is raised.
        If the simulation is running, it will be cancelled and a HTTPException with status code 200 and detail "Simulation stopped" is raised.
    """
    global future
    if future is None:
        logger.debug("No simulation running and is alive")
        raise HTTPException(status_code=200, detail=f"No simulation running")
    elif future.running():
        logger.debug("Simulation is running and is alive")
        future.cancel()
        logger.debug("Simulation stopped")
        raise HTTPException(status_code=200, detail=f"Simulation stopped")
    ProcessPoo.shutdown(wait=True)
    return JSONResponse(content="Simulation stopped", status_code=200)


@router.post("/update_all_params")
def update_item(response: ParameterRequest):
    """
    Update stored_params and configs based on the given response.

    Parameters
    ----------
    response : ParameterRequest
        The response object containing the updated parameters and configurations.

    Returns
    -------
    JSONResponse
        A JSON response indicating that the parameters have been updated.

    """
    # Handle run parameters
    global stored_params

    if "run" in response and response.run is not None:
        stored_params = {
            key: value
            for key, value in response.run.model_dump().items()
            if value is not None
        }
    print()

    # Handle config_variables
    if "config" in response and response.config is not None:
        configs.config = configs.set_config(response.config.model_dump())
    return JSONResponse(
        content="Parameters Updated", status_code=status.HTTP_202_ACCEPTED
    )


def reset():
    """
    Resets the stored parameters to None.

    Parameters:
    None

    Returns:
    None
    """
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
