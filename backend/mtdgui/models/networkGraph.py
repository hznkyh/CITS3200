from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Host(BaseModel):
    os_type: str
    os_version: str
    host_ip: str
    host_id: int
    p_u_compromise: bool
    total_users: int
    uuid: str
    total_services: int
    total_nodes: int
    compromised: bool
    compromised_services: List


class Node(BaseModel):
    subnet: int
    layer: int
    host: Host
    id: int


class Link(BaseModel):
    source: int
    target: int


class NetworkGraph(BaseModel):
    directed: bool
    multigraph: bool
    graph: Dict[str, Any]
    nodes: List[Node]
    links: List[Link]
    
class NetworkGraphs(BaseModel):
    graphs: List[NetworkGraph]
