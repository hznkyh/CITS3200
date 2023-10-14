from pydantic import BaseModel
from typing import Union, List

class graphName(BaseModel):
    """
    A class representing a graph number.

    Parameters
    ----------
    graph_name : str
        The string key identifying the graph.

    Attributes
    ----------
    graph_name : str
        The string key identifying the graph.
    """
    graph_name: str


class MTD_PRIORITY(BaseModel):
    """
    A class representing the priority of various MTD (Moving Target Defense) techniques.

    Attributes
    ----------
    CompleteTopologyShuffle : Union[int, None]
        The priority of complete topology shuffle technique.
    HostTopologyShuffle : Union[int, None]
        The priority of host topology shuffle technique.
    IPShuffle : Union[int, None]
        The priority of IP shuffle technique.
    OSDiversity : Union[int, None]
        The priority of OS diversity technique.
    PortShuffle : Union[int, None]
        The priority of port shuffle technique.
    ServiceDiversity : Union[int, None]
        The priority of service diversity technique.
    UserShuffle : Union[int, None]
        The priority of user shuffle technique.
    """
    CompleteTopologyShuffle: Union[int, None]
    HostTopologyShuffle: Union[int, None]
    IPShuffle: Union[int, None]
    OSDiversity: Union[int, None]
    PortShuffle: Union[int, None]
    ServiceDiversity: Union[int, None]
    UserShuffle: Union[int, None]

class MTD_TRIGGER_INTERVAL(BaseModel):
    """
    A class representing the trigger intervals for a MTD (Moving Target Defense) system.

    Attributes
    ----------
    simultaneous : Union[List[float], None]
        A list of simultaneous trigger intervals, or None if there are none.
    random : Union[List[float], None]
        A list of random trigger intervals, or None if there are none.
    alternative : Union[List[float], None]
        A list of alternative trigger intervals, or None if there are none.
    """
    simultaneous: Union[List[float], None]
    random: Union[List[float], None]
    alternative: Union[List[float], None]

class ConfigModel(BaseModel):
    """
    A model representing configuration settings for MTD (Moving Target Defense).

    Attributes
    ----------
    MTD_PRIORITY : Union[MTD_PRIORITY, None]
        The priority level for MTD.
    MTD_TRIGGER_INTERVAL : Union[MTD_TRIGGER_INTERVAL, None]
        The interval at which MTD triggers.
    """
    MTD_PRIORITY: Union[MTD_PRIORITY,None]
    MTD_TRIGGER_INTERVAL: Union[MTD_TRIGGER_INTERVAL,None]

class RunModel(BaseModel):
    """
    A data model representing the parameters for running a simulation.

    Parameters
    ----------
    total_nodes : int
        The total number of nodes in the simulation.
    total_endpoints : int
        The total number of endpoints in the simulation.
    total_layers : int
        The total number of layers in the simulation.
    terminate_compromise_ratio : float
        The ratio of compromised nodes at which the simulation should terminate.
    scheme : str
        The MTD scheme to use in the simulation.
    mtd_interval : float
        The interval at which to apply the MTD scheme.
    finish_time : float
        The time at which the simulation should finish.
    checkpoints : int
        The number of checkpoints to save during the simulation.
    total_subnets : int or None
        The total number of subnets in the simulation, or None if there are no subnets.
    target_layer : int or None
        The target layer for the simulation, or None if there is no target layer.
    """
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
    """
    A class representing a request for a parameter.

    Parameters
    ----------
    graph : graphName
        The number of the graph.
    run : RunModel
        The run model.
    config : Union[ConfigModel, None]
        The configuration model, or None if not specified.
    """
    graph: graphName
    run: RunModel
    config: Union[ConfigModel,None]
