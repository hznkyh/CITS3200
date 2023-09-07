from fastapi import APIRouter, HTTPException
import simpy
import threading

router = APIRouter(
    prefix="/develop",
    tags=["develop"],
    responses={404: {"description": "Not found"}}
)

env = simpy.Environment()
simulation_thread = None
simulation_speed = 1.0


def car(env, speed):
    global simulation_speed
    while True:
        print('Start parking at %d' % env.now)
        parking_duration = 5 / speed
        yield env.timeout(parking_duration)

        print('Start driving at %d' % env.now)
        trip_duration = 2 / speed
        yield env.timeout(trip_duration)


@router.get("/")
async def read_items():
    return "Hello World to car simulation"


@router.post("/start")
def start_simulation():
    global simulation_thread, env, simulation_speed
    if simulation_thread is not None:
        raise HTTPException(
            status_code=400, detail="Simulation already running")
    env.process(car(env, simulation_speed))
    simulation_thread = threading.Thread(target=env.run, args=([5]))
    simulation_thread.start()
    return {"status": "Simulation started"}


@router.post("/stop")
def stop_simulation():
    global simulation_thread, env
    if simulation_thread is None:
        raise HTTPException(status_code=400, detail="No simulation running")
    env.timeout(0)
    simulation_thread.join()
    simulation_thread = None
    env = simpy.Environment()  # create a new environment
    return {"status": "Simulation stopped"}


@router.post("/speed/{speed}")
def set_speed(speed: float):
    global simulation_speed
    if speed <= 0:
        raise HTTPException(
            status_code=400, detail="Speed must be greater than 0")
    simulation_speed = speed
    return {"status": "Simulation speed set to " + str(speed)}
