import logging
import time
from typing import Annotated, List, Dict
from auth import get_current_active_user
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from concurrent.futures import Future
from concurrent.futures import ProcessPoolExecutor, as_completed
from threading import Lock
from controllers import serialize_graph
from models import User, ParameterRequest
from sessions import sessions
import copy
from controllers.pools import handleRequest

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/network", tags=["network"], responses={404: {"description": "Not found"}}
)

# initializing variables
futuresComplete = False
messageQueueLock = Lock()
messageQueue = []
set_params = None

#   !Removed this function because it was causing the server to crash
# def checkFuturesCompletion(futures: dict[Future, int], uuid):
#     """
#     The function `checkFuturesCompletion` checks the completion status of a list of futures and adds
#     their results to a message queue.

#     Parameters
#     ----------
#     futures
#         The `futures` parameter is a list of `concurrent.futures.Future` objects. These objects represent
#     asynchronous tasks that are being executed concurrently.

#     """
#     global futuresComplete
#     doneFutures = set()
#     messages = []
#     logger.debug("Started checking futures' completion")

#     # responsible for checking the completion status of a list of futures and adding their results to
#     # a message queue.
#     while not futuresComplete:
#         for future, id in futures.items():
#             if future.done() and future not in doneFutures:
#                 doneFutures.add(future)
#                 result = future.result()  # Get the result of the future
#                 # print(result, id)
#                 logger.debug(
#                     f"Future {futures[future]} completed with result: {result}."
#                 )
#                 messages.append(result)
#                 with messageQueueLock:  # Safely add the result to the message queue
#                     messageQueue.append(result)

#         if len(doneFutures) == len(futures):
#             futuresComplete = True
#             logger.debug("All futures are completed.")
#         time.sleep(1)

#     logger.debug("Stopped checking futures' completion.")
#     sessions[uuid]["evaluation"] = [
#         copy.deepcopy(message["evaluation"]) for message in messages
#     ]
#     sessions[uuid]["snapshots"] = [
#         copy.deepcopy(message["snapshots"]) for message in messages
#     ]


@router.post("/multi-graph-params")
async def get_prams(
    params: Dict[str,ParameterRequest],
):
    global set_params
    print("Got params",params)
    set_params = params
    return JSONResponse(content="prams set" , status_code=status.HTTP_202_ACCEPTED)


@router.get("/multi-graph")
async def get_graph(client: Annotated[User, Depends(get_current_active_user)]):
    global set_params
    params = set_params

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(handleRequest, name, request) for name, request in params.items()]
        results = [future.result() for future in as_completed(futures)]
        
        # print(results)
        
        logger.debug("Stopped checking futures' completion.")

        sessions[client.uuid]["snapshots"] = {
            result[0]:copy.deepcopy(result[1]["snapshots"]) for result in results
        }
        
        sessions[client.uuid]["evaluation"] = {
            result[0]:copy.deepcopy(result[1]["evaluation"]) for result in results
        }


    try:
        
        response = {
            graphName: [serialize_graph(graph_item) for graph_item in graph]
            for graphName,graph in sessions[client.uuid]["snapshots"].items()
            
        }
        
        logger.debug(f"Returning result: {response}")
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except IndexError:
        logger.error("Result not found")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Result not found"
        )


@router.get("/result/{index}")
async def get_result(
    index: int, client: Annotated[User, Depends(get_current_active_user)]
):
    try:
        response = [
            serialize_graph(graph)
            for graph in sessions[client.uuid]["snapshots"][index]
        ]
        logger.debug(f"Returning result: {response}")
        return JSONResponse(content=response, status_code=status.HTTP_202_ACCEPTED)
    except IndexError:
        logger.error("Result not found")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Result not found"
        )


@router.get("/evaluation/{index}")
async def get_result(
    index: int, client: Annotated[User, Depends(get_current_active_user)]
):
    try:
        evaluation = sessions[client.uuid]["evaluation"][index]
        response = evaluation.compromised_num()
        print(response)
        logger.debug(f"Returning result: {response}")
        return JSONResponse(content=response, status_code=status.HTTP_202_ACCEPTED)
    except IndexError:
        logger.error("Result not found")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Result not found"
        )


@router.post("/config")
async def get_config(
    prams: List[ParameterRequest],
    client: Annotated[User, Depends(get_current_active_user)],
):
    print(prams)

    # Handle run parameters
    global stored_params
    run_params = [pram.run.model_dump() for pram in prams]
    stored_params = [
        {key: value for key, value in pram.items() if value is not None}
        for pram in run_params
    ]

    return JSONResponse(content=stored_params, status_code=status.HTTP_202_ACCEPTED)

@router.post("/remove/{graph_name}")
def remove_graph(
    client: Annotated[User, Depends(get_current_active_user)],
    graph_name : str
):
    if (sessions[client.uuid]["evaluation"][graph_name] is not None):
        sessions[client.uuid]["evaluation"][graph_name] = None