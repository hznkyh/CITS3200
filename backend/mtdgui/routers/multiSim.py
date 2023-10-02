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

def checkFuturesCompletion(futures: dict[Future, int], uuid):
    """
    The function `checkFuturesCompletion` checks the completion status of a list of futures and adds
    their results to a message queue.

    Parameters
    ----------
    futures
        The `futures` parameter is a list of `concurrent.futures.Future` objects. These objects represent
    asynchronous tasks that are being executed concurrently.

    """
    global futuresComplete
    doneFutures = set()
    messages = []
    logger.debug("Started checking futures' completion")

    # responsible for checking the completion status of a list of futures and adding their results to
    # a message queue.
    while not futuresComplete:
        for future, id in futures.items():
            if future.done() and future not in doneFutures:
                doneFutures.add(future)
                result = future.result()  # Get the result of the future
                # print(result, id)
                logger.debug(
                    f"Future {futures[future]} completed with result: {result}."
                )
                messages.append(result)
                with messageQueueLock:  # Safely add the result to the message queue
                    messageQueue.append(result)

        if len(doneFutures) == len(futures):
            futuresComplete = True
            logger.debug("All futures are completed.")
        time.sleep(1)

    logger.debug("Stopped checking futures' completion.")
    sessions[uuid]["evaluation"] = [
        copy.deepcopy(message["evaluation"]) for message in messages
    ]
    sessions[uuid]["snapshots"] = [
        copy.deepcopy(message["snapshots"]) for message in messages
    ]


@router.post("/multi-graph-params")
async def get_prams(
    params: List[ParameterRequest],
    client: Annotated[User, Depends(get_current_active_user)],
):
    # test_config = {
    #     "MTD_PRIORITY": {
    #         "CompleteTopologyShuffle": 0,
    #         "HostTopologyShuffle": 0,
    #         "IPShuffle": 0,
    #         "OSDiversity": 0,
    #         "PortShuffle": 0,
    #         "ServiceDiversity": 0,
    #         "UserShuffle": 0,
    #     },
    #     "MTD_TRIGGER_INTERVAL": {
    #         "simultaneous": [0],
    #         "random": [0],
    #         "alternative": [0],
    #     },
    # }

    # test_parameters = parameters | dict(
    #     Parameters(checkpoints=list(range(0, 3000, 1000)))
    # )
    # listParams = {
    #     i: params for i, params in enumerate(itertools.repeat(test_parameters, 2))
    # }
    print("CLIENT IS ", client.uuid)
    # with ProcessPoolExecutor() as executor:
    #     futures = [executor.submit(handleRequest, req) for req in params]
    #     results = [future.result() for future in as_completed(futures)]
    global set_params
    set_params = params
    print("PARAMS LOADED AS " , params)

    # for i in results: 
    #     print(i)
    # dict_run = [{"run": item, "config": test_config} for item in listParams.values()]
    return JSONResponse(content='results')


@router.get("/multi-graph")
async def get_graph(
    client: Annotated[User, Depends(get_current_active_user)]
):
    print("CLIENT IS ", client.uuid)
    global set_params
    params = set_params
    print("PARAMS SET TO " , params)
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(handleRequest, req) for req in params]
        results = [future.result() for future in as_completed(futures)]
    for i in results: 
        print(i)
    return {"status": "completed", "params": params}    
#     # The code block you provided is creating a list of parameters (`listParams`) using the
#     # `itertools.repeat()` function. The `itertools.repeat()` function returns an iterator that repeats
#     # the specified value (`parameters` in this case) a specified number of times (`10` in this case).
#     # print(prams)
#     # final_params = parameters

#     # if "checkpoints" in final_params:
#     #     if type(final_params["checkpoints"]) is int:
#     #         final_params["checkpoints"] = range(
#     #             final_params["start_time"],
#     #             int(final_params["finish_time"]),
#     #             final_params["checkpoints"],
#     #         )
#     # # listParams = itertools.repeat(final_params, 2)
#     # print(prams)

#     # futuresList = {
#     #     ProcessPoo.get_pool().submit(create_sim, **params): i
#     #     for i, params in enumerate(prams)
#     # }
#     # logger.debug(f"Submitted {len(futuresList)} tasks to ProcessPoolExecutor.")

#     # futuresChecker = Thread(
#     #     target=checkFuturesCompletion, args=(futuresList, client.uuid)
#     # )
#     # futuresChecker.start()
#     # logger.debug("Started futures checker thread.")

#     # futuresChecker.join()
#     # logger.debug("Futures checker thread completed.")
#     # # ProcessPoo.shutdown()
#     return {"status": "completed", "number_of_results": len(messageQueue)}


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

    # #Handle config_variables
    # config_params = prams.config
    # if (item.config is not None):
    #     config_params = config_params.model_dump()
    # configs.config = configs.set_config(config_params)
    return JSONResponse(content=stored_params, status_code=status.HTTP_202_ACCEPTED)
