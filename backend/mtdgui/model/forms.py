from pydantic import BaseModel
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
    total_nodes: float
    total_endpoints: float
    total_layers: float
    terminate_compromise_ratio: float
    scheme: str
    mtd_interval: float