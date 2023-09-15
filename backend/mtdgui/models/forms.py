from pydantic import BaseModel, validator
from typing import Union, Optional,Any

class Item(BaseModel):
    configVal: float

class MTD_PRIORITYItem(BaseModel):
    CompleteTopologyShuffle: Union[int, None]
    HostTopologyShuffle: Union[int, None]
    IPShuffle: Union[int, None]
    OSDiveristy: Union[int, None]
    PortShuffle: Union[int, None]
    ServiceDiversity: Union[int, None]
    UserShuffle: Union[int, None]

class MTD_TRIGGERItem(BaseModel):
    simultaneous: Union[float, None]
    random: Union[float, None]
    alternative: Union[float, None]

class formData(BaseModel):
    total_nodes: int
    total_endpoints: int
    total_layers: int
    terminate_compromise_ratio: float
    scheme: str
    mtd_interval: float
    finish_time: float
    checkpoints: int
    total_subnets: Union[int, None]
    target_layers: Union[int, None]
    MTD_PRIORITY: Any = None
    MTD_TRIGGER_INTERVAL: Any = None