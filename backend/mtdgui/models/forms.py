from pydantic import BaseModel
from typing import Union, List

class graphName(BaseModel):
    graph_name: str

class MTD_PRIORITY(BaseModel):
    CompleteTopologyShuffle: Union[int, None]
    HostTopologyShuffle: Union[int, None]
    IPShuffle: Union[int, None]
    OSDiversity: Union[int, None]
    PortShuffle: Union[int, None]
    ServiceDiversity: Union[int, None]
    UserShuffle: Union[int, None]

class MTD_TRIGGER_INTERVAL(BaseModel):
    simultaneous: Union[List[float], None]
    random: Union[List[float], None]
    alternative: Union[List[float], None]

class ConfigModel(BaseModel):
    MTD_PRIORITY: Union[MTD_PRIORITY,None]
    MTD_TRIGGER_INTERVAL: Union[MTD_TRIGGER_INTERVAL,None]

class RunModel(BaseModel):
    total_nodes: int
    total_endpoints: int
    total_layers: int
    terminate_compromise_ratio: float
    scheme: str
    mtd_interval: float
    finish_time: float
    checkpoints: int
    total_subnets: Union[int, None]
    target_layer: Union[int, None]

class ParameterRequest(BaseModel):
    graph: graphName
    run: RunModel
    config: Union[ConfigModel,None]
