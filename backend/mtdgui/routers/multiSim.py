import itertools
import logging
import sys
import time
from concurrent.futures import Future
from pathlib import Path
from threading import Lock, Thread
from typing import Annotated, Any
from auth import get_current_active_user
from models import User
from controllers.loggerConfig import setup_logger

# Setup the logger
logger = logging.getLogger(__name__)
setup_logger(logger)

# from models.forms import Item,MTD_PRIORITYItem,formData
from models.forms import ParameterRequest
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, Depends, HTTPException
from itertools import chain, count

from concurrent.futures import ProcessPoolExecutor
from fastapi import APIRouter, HTTPException
import logging
from controllers.loggerConfig import setup_logger
from models.forms import ParameterRequest
import itertools
import time
from threading import Thread, Lock

# from networkx.utils import to_tuple
from controllers.serialiser import serialize_graph
import sys
from simulator.adapter import create_sim
from sessions import sessions

router = APIRouter(
    prefix="/network", tags=["network"], responses={404: {"description": "Not found"}}
)

# initializing variables
futuresComplete = False
messageQueueLock = Lock()
messageQueue = []

POOL = ProcessPoolExecutor(max_workers=2)  # Assuming 4 processes for simplicity
parameters = {
    "start_time": 0,
    "finish_time": 3000,
    "checkpoints": range(0, 3000, 1000),
    "new_network": True,
    "scheme": "random",
    "mtd_interval": 4,
    "custom_strategies": None,
    "total_nodes": 20,
    "total_endpoints": 5,
    "total_subnets": 8,
    "total_layers": 4,
    "target_layer": 4,
    "total_database": 2,
    "terminate_compromise_ratio": 0.8,
}
# ... [rest of your imports and setup]

def checkFuturesCompletion(futures:dict[Future, int], uuid):
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
    messages =[]
    logger.debug("Started checking futures' completion")

    # responsible for checking the completion status of a list of futures and adding their results to
    # a message queue.
    while not futuresComplete:
        for future in futures:
            if future.done() and future not in doneFutures:
                doneFutures.add(future)
                result = future.result()  # Get the result of the future
                logger.debug(
                    f"Future {futures[future]} completed with result: {result}."
                )
                messages.append(result)
                with messageQueueLock:  # Safely add the result to the message queue
                    messageQueue.append(result)

        # The code block `if len(doneFutures) == len(futures): futuresComplete = True` is checking if all the
        # futures in the `futures` list have completed. If the number of completed futures (`doneFutures`) is
        # equal to the total number of futures (`len(futures)`), it means that all the futures have completed
        # their execution. In that case, the `futuresComplete` flag is set to `True` to indicate that all the
        # futures are completed. This flag is used in the `checkFuturesCompletion` function to determine when
        # to stop checking the completion status of the futures.
        if len(doneFutures) == len(futures):
            futuresComplete = True
            logger.debug("All futures are completed.")
        time.sleep(1)
    logger.debug("Stopped checking futures' completion.")
    print(messages)
    # sessions[uuid]['status'] = "completed"
    # sessions[uuid]["evaluation"] = [ message for  in messages]
    # sessions[uuid]["snapshots"] = "completed"


@router.get("/muti-graph-prams")
async def get_prams():
    listParams = itertools.repeat(parameters, 4)
    yield JSONResponse(content={"result": listParams})

@router.get("/muti-graph")
async def get_graph(
    client: Annotated[User, Depends(get_current_active_user)]
                    ):
    global POOL
    # The code block you provided is creating a list of parameters (`listParams`) using the
    # `itertools.repeat()` function. The `itertools.repeat()` function returns an iterator that repeats
    # the specified value (`parameters` in this case) a specified number of times (`10` in this case).

    listParams = itertools.repeat(parameters, 4)

    futuresList = {
        POOL.submit(create_sim, **params): i
        for i, params in enumerate(listParams)
    }
    logger.info(f"Submitted {len(futuresList)} tasks to ProcessPoolExecutor.")

    futuresChecker = Thread(target=checkFuturesCompletion, args=(futuresList,client.uuid))
    futuresChecker.start()
    logger.info("Started futures checker thread.")
    
    futuresChecker.join()
    logger.info("Futures checker thread completed.")
    POOL.shutdown(wait=True)
    return {"status": "completed", "number_of_results": len(messageQueue)}


@router.get("/result/{index}")
async def get_result(index: int):
    with messageQueueLock:
        try:
            print(messageQueue[index])
            return JSONResponse(content={"result":"23"})
        except IndexError:
            raise HTTPException(status_code=404, detail="Result not found")
        

@router.get("/evaluation/{index}")
async def get_result(index: int):
    with messageQueueLock:
        try:
            print(messageQueue[index])
            return JSONResponse(content={"result": "12"})
            # return JSONResponse(content={"result": messageQueue[index]})
        except IndexError:
            raise HTTPException(status_code=404, detail="Result not found")