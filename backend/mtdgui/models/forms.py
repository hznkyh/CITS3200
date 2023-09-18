from pydantic import BaseModel, conint
from typing import Optional, Union, List
# class MTD_PRIORITY(BaseModel):
#     CompleteTopologyShuffle: Optional[conint(ge=0)] = None
#     HostTopologyShuffle: Optional[conint(ge=0)] = None
#     IPShuffle: Optional[conint(ge=0)] = None
#     OSDiveristy: Optional[conint(ge=0)] = None
#     PortShuffle: Optional[conint(ge=0)] = None
#     ServiceDiversity: Optional[conint(ge=0)] = None
#     UserShuffle: Optional[conint(ge=0)] = None

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
    run: RunModel
    config: Union[ConfigModel,None]
# from pydantic import BaseModel, validator
# from typing import Union, Optional,Any

# class Item(BaseModel):
#     configVal: float

# class MTD_PRIORITYItem(BaseModel):
#     CompleteTopologyShuffle: Union[int, None]
#     HostTopologyShuffle: Union[int, None]
#     IPShuffle: Union[int, None]
#     OSDiveristy: Union[int, None]
#     PortShuffle: Union[int, None]
#     ServiceDiversity: Union[int, None]
#     UserShuffle: Union[int, None]

# class MTD_TRIGGERItem(BaseModel):
#     simultaneous: Union[float, None]
#     random: Union[float, None]
#     alternative: Union[float, None]

# class formData(BaseModel):
#     total_nodes: int
#     total_endpoints: int
#     total_layers: int
#     terminate_compromise_ratio: float
#     scheme: str
#     mtd_interval: float
#     finish_time: float
#     checkpoints: int
#     total_subnets: Union[int, None]
#     target_layers: Union[int, None]
#     MTD_PRIORITY: Any = None
#     MTD_TRIGGER_INTERVAL: Any = None
