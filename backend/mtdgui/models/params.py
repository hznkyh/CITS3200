from typing import List, Optional
from pydantic import BaseModel

class Parameters(BaseModel):
    """
    A class representing the parameters for the MTD simulation.

    Parameters
    ----------
    start_time : int, optional
        The start time of the simulation, by default 0.
    finish_time : int, optional
        The finish time of the simulation, by default 3000.
    checkpoints : List[int], optional
        A list of times at which to record the state of the simulation, by default
        [0, 1000, 2000, 3000].
    new_network : bool, optional
        Whether to generate a new network for the simulation, by default True.
    scheme : str, optional
        The MTD scheme to use, by default "random".
    mtd_interval : int, optional
        The interval at which to perform MTD, by default 4.
    custom_strategies : Optional[List[str]], optional
        A list of custom MTD strategies to use, by default None.
    total_nodes : int, optional
        The total number of nodes in the network, by default 20.
    total_endpoints : int, optional
        The total number of endpoints in the network, by default 5.
    total_subnets : int, optional
        The total number of subnets in the network, by default 8.
    total_layers : int, optional
        The total number of layers in the network, by default 4.
    target_layer : int, optional
        The target layer for MTD, by default 4.
    total_database : int, optional
        The total number of databases in the network, by default 2.
    terminate_compromise_ratio : float, optional
        The ratio of compromised nodes at which to terminate the simulation, by default 0.8.
    """
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

