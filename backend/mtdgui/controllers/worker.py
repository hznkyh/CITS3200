from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue, Event
import logging

# Setting up the logger
logger = logging.getLogger(__name__)

class ProcessPoo:
    """
    A class that implements a Singleton design pattern for ProcessPoolExecutor.

    Attributes:
    _instance (SingletonExecutor): The SingletonExecutor instance.
    _pool (ProcessPoolExecutor): The ProcessPoolExecutor instance.
    """

    _instance = None
    _pool = None

    def __new__(cls):
        """
        Creates a new instance of SingletonExecutor if it does not exist.

        Returns:
        SingletonExecutor: The SingletonExecutor instance.
        """
        if cls._instance is None:
            cls._instance = super(ProcessPoo, cls).__new__(cls)
            cls._pool = ProcessPoolExecutor(max_workers=2)
            logger.info("Initialized ProcessPoolExecutor.")
        return cls._instance

    @classmethod
    def get_pool(cls):
        """
        Returns the ProcessPoolExecutor instance.

        Returns:
        ProcessPoolExecutor: The ProcessPoolExecutor instance.
        """
        return cls._pool

    @classmethod
    def shutdown(cls, wait=True):
        """
        Shuts down the ProcessPoolExecutor instance.

        Args:
        wait (bool): Whether to wait for all running tasks to complete before shutting down.
        """
        if cls._pool:
            cls._pool.shutdown(wait)
            logger.debug("Shutdown ProcessPoolExecutor.")
