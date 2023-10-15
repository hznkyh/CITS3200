from pydantic_settings import BaseSettings
from models import Parameters

class Settings(BaseSettings):
    """
    A class representing the settings for the backend of the MTDGUI project.

    Attributes
    ----------
    SECRET_KEY : str
        A string representing the secret key used for encryption.
    ALGORITHM : str
        A string representing the algorithm used for encryption.
    ACCESS_TOKEN_EXPIRE_MINUTES : int
        An integer representing the number of minutes before an access token expires.
    """
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str  = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

parameters = {
    "start_time": 0,
    "finish_time": 10000,
    "checkpoints": range(0, 10000, 1000),
    "new_network": True,
    "scheme": 'random',
    "mtd_interval": None,
    "custom_strategies": None,
    "total_nodes": 50,
    "total_endpoints": 5,
    "total_subnets": 8,
    "total_layers": 4,
    "target_layer": 4,
    "total_database": 2,
    "terminate_compromise_ratio": 0.8
}

settings = Settings()
