from pydantic import BaseModel
from typing import List, Optional

class Parameters(BaseModel):
    start_time: int = 0
    finish_time: int = 3000
    checkpoints: List[int] = list(range(0, 3000, 1000))
    new_network: bool = True
    scheme: str = "random"
    mtd_interval: int = 4
    custom_strategies: Optional[List[str]] = None
    total_nodes: int = 20
    total_endpoints: int = 5
    total_subnets: int = 8
    total_layers: int = 4
    target_layer: int = 4
    total_database: int = 2
    terminate_compromise_ratio: float = 0.8

