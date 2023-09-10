from pydantic import BaseModel, validator
from typing import Union, Optional

class Item(BaseModel):
    configVal: float

class MTD_PRIORITYItem(BaseModel):
    CompleteTopologyShuffle: Union[float, None]
    HostTopologyShuffle: Union[float, None]
    IPShuffle: Union[float, None]
    OSDiveristy: Union[float, None]
    PortShuffle: Union[float, None]
    ServiceDiversity: Union[float, None]
    UserShuffle: Union[float, None]

class formData(BaseModel):
    total_nodes: Union[int, None] = None
    total_endpoints: Union[int, None] = None
    total_layers: Union[int, None] = None
    terminate_compromise_ratio: Union[float, None] = None
    scheme: Union[str, None] = None
    mtd_interval: Union[float, None] = None
    class Config:
        validate_assignment = True