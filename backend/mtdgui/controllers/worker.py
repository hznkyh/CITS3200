from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue, Event
import logging

# Setting up the logger
logger = logging.getLogger(__name__)
task_queue = Queue()
exit_signal = Event()

def worker():
    """The function executed by each process."""
    while not exit_signal.is_set():
        try:
            # Get a task from the queue and execute it
            task = task_queue.get(timeout=1)  # waits for 1 second for a task
            task()  # Assuming the task is a callable function
            logger.info("Task executed successfully.")
        except Exception as e:
            logger.error(f"Error executing task: {e}")

executor = None

def start_worker_processes():
    global executor
    logger.info("Starting worker processes...")
    executor = ProcessPoolExecutor(max_workers=3)
    for _ in range(3):  # or however many processes you want
        executor.submit(worker)
    logger.info("Worker processes started.")

def shutdown_worker_processes():
    logger.info("Shutting down worker processes...")
    exit_signal.set()
    executor.shutdown(wait=True)
    logger.info("Worker processes shut down.")

def add_task_to_worker(task):
    """Utility function to add a task to the worker processes."""
    logger.info("Adding task to worker.")
    task_queue.put(task)
