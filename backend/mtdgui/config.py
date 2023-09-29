from pydantic_settings import BaseSettings

from models import Parameters


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str  = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

parameters = {
    "start_time": 0,
    "finish_time": 3000,
    "checkpoints": 1000,
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

settings = Settings()

parameters:Parameters = parameters
