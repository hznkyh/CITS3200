import copy
import logging
from auth import get_current_active_user
from models.forms import ParameterRequest
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from controllers import serialize_graph, handleRequest
from models import User, ParameterRequest
from simulator import create_sim, configs
from typing import Annotated, Union, Dict
from config import parameters
from sessions import sessions
from concurrent.futures import Future, ProcessPoolExecutor, as_completed

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/network", tags=["network"], responses={404: {"description": "Not found"}}
)
future: Union[Future, None] = None
stored_params = None

@router.post("/graph-params")
async def update_item(
    params: ParameterRequest,
):
    global stored_params
    stored_params = {1: params}
    return JSONResponse(content="prams set" , status_code=status.HTTP_202_ACCEPTED)


@router.get("/graph")
async def get_graph(client: Annotated[User, Depends(get_current_active_user)]):
    global stored_params
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(handleRequest, name, request) for name, request in stored_params.items()]
        results = [future.result() for future in as_completed(futures)][0]        
        logger.debug("Stopped checking futures' completion.")      
        sessions[client.uuid]['single'] = {
            'name' : results[0],
            'snapshots' : copy.deepcopy(results[1]["snapshots"]),
            'evaluation' : copy.deepcopy(results[1]["evaluation"])
        }
    try:
        graphName = sessions[client.uuid]['single']['name']
        response = {
            graphName: [serialize_graph(graph_item) for graph_item in sessions[client.uuid]['single']["snapshots"]]            
        }
        logger.debug(f"Returning result: {response}")
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except IndexError:
        logger.error("Result not found")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Result not found"
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
