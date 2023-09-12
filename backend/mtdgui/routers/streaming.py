from threading import Lock, Thread
import random
from fastapi import APIRouter, WebSocket, Depends, HTTPException
from backend.mtdgui.dev.Sim import MySimulator
from starlette.responses import StreamingResponse
import time

router = APIRouter(
    prefix="/streaming",
    tags=["streaming"],
    responses={404: {"description": "Not found"}}
)

# Create a shared list using Manager
message_queue = [] # This will hold our messages from the simulation
message_queue_lock = Lock() 

def stream_messages(thread):
    '''The function `stream_messages` continuously checks for messages in a queue and yields them as a data
    stream, while also checking if a separate thread is still running.
    
    Parameters
    ----------
    thread
        The "thread" parameter is an instance of a thread object. It is used to check if the thread is
    still alive or has completed its execution.
    
    '''
    while True:
        with message_queue_lock:
            # print("Inside stream_messages")
            # print("thread.is_alive",thread.is_alive())
            # print(message_queue)
            if message_queue:  # Check if there are messages to send
                msg = message_queue.pop(0) # Retrieve the first message
                yield f"data: {msg}\n\n"
            else:
                if ~thread.is_alive():  # Check if thread have completed
                    break
                else:
                    time.sleep(1)  # Wait a bit before checking again


# This callback will append simulation data to our message queue
def sse_callback(name:str, typeof:str, wait:float):
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
    # print("Inside sse_callback")
    # print(name,typeof,wait)
    if(typeof != "Wait Finished"):
        # print(f"Notification: {name} reneged after waiting for {wait:.3f} time units.")
        msg= f"Notification: {name} reneged after waiting for {wait:.3f} time units."
    else :
        # print(f"Notification: {name} Wait Finished at {wait:.3f} time units.")
        msg= f"Notification: {name} Wait Finished at {wait:.3f} time units."
    with message_queue_lock:
        message_queue.append(msg)
        # print(message_queue)


@router.get("/stream/")
async def stream_simulation_data():
    '''The function `stream_simulation_data` runs a simulation using a separate thread and returns a
    streaming response in the form of a text/event-stream.
    
    Returns
    -------
        a StreamingResponse object with a media type of "text/event-stream".
    
    '''
    # Use the Thread class to run the simulation
    seeds = [random.randint(1, 1000) for _ in range(1)]
    sim = MySimulator(seeds[0],callback=sse_callback, debug=False)
    thread = Thread(target=sim.run, args=(50,))
    thread.start()

    thread.join()  # This waits for each thread to complete

    # The line `return StreamingResponse(stream_messages(thread), media_type="text/event-stream")` is
    # creating a streaming response object with a media type of "text/event-stream".
    return StreamingResponse(stream_messages(thread), media_type="text/event-stream")
