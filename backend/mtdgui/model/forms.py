from pydantic import BaseModel
from typing import Union, Optional

class Item(BaseModel):
    configVal: float

class MTD_PRIORITYItem(BaseModel):
    CompleteTopologyShuffle: Optional[float]
    HostTopologyShuffle: Optional[float]
    IPShuffle: Optional[float]
    OSDiveristy: Optional[float]
    PortShuffle: Optional[float]
    ServiceDiversity: Optional[float]
    UserShuffle: Optional[float]

class formData(BaseModel):
    total_nodes: float
    total_endpoints: float
    total_layers: float
    terminate_compromise_ratio: float
    scheme: str
    mtd_interval: float
    MTD_PRIORITY: Union[MTD_PRIORITYItem, None]