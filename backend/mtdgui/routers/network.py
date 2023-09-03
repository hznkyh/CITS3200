import json
import networkx as nx
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from itertools import chain, count
from networkx.utils import to_tuple
import simpy


import sys
import os
from pathlib import Path
# Construct the path to the "s" directory
s_directory = os.path.join(Path(__file__).parents[3], "simulator")
# Add the "s" directory to the Python path
sys.path.append(s_directory)
from adapter import *

#
# from adapter import sim_params, run_sim

router = APIRouter(prefix="/network",
                   tags=["network"], responses={404: {"description": "Not found"}})

# env = simpy.Environment()
env = simpy.Environment()
simulation_thread = None
simulation_speed = 1.0
_attrs = dict(source="source", target="target", name="id", key="key", link="links")


class CustomNode:
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute

    def to_dict(self):
        #    return {"name": self.name, "attribute": self.attribute}
        return self.__dict__
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)




def serialize_graph(G:nx.Graph, attrs=None):
    """Returns data in node-link format that is suitable for JSON serialization
    and use in Javascript documents.

    Parameters
    ----------
    G : NetworkX graph

    attrs : dict
        A dictionary that contains five keys 'source', 'target', 'name',
        'key' and 'link'.  The corresponding values provide the attribute
        names for storing NetworkX-internal graph data.  The values should
        be unique.  Default value::

            dict(source='source', target='target', name='id',
                 key='key', link='links')

        If some user-defined graph data use these attribute names as data keys,
        they may be silently dropped.

    Returns
    -------
    data : dict
       A dictionary with node-link formatted data.

    Raises
    ------
    NetworkXError
        If values in attrs are not unique.

    Examples
    --------

    Notes
    -----
    Graph, node, and link attributes are stored in this format.  Note that
    attribute keys will be converted to strings in order to comply with JSON.
    """
    multigraph = G.is_multigraph()
    # Allow 'attrs' to keep default values.
    if attrs is None:
        attrs = _attrs
    else:
        attrs.update({k: v for (k, v) in _attrs.items() if k not in attrs})
    name = attrs["name"]
    source = attrs["source"]
    print(source)
    target = attrs["target"]
    links = attrs["link"]
    # Allow 'key' to be omitted from attrs if the graph is not a multigraph.
    key = None if not multigraph else attrs["key"]
    if len({source, target, key}) < 3:
        raise nx.NetworkXError("Attribute names are not unique.")
    data = {
        "directed": G.is_directed(),
        "multigraph": multigraph,
        "graph": G.graph,
        "nodes": [dict(chain(G.nodes[n].items(), [(name, n.to_dict())])) for n in G],
    }
    if multigraph:
        data[links] = [
            dict(chain(d.items(), [(source, u.to_dict()), (target, v), (key, k)]))
            for u, v, k, d in G.edges(keys=True, data=True)
        ]
    else:            
        data[links] = [
            dict(chain(d.items(), [(source, u.to_dict()), (target, v.to_dict())]))
            for u, v, d in G.edges(data=True)
        ]
    return data





def serialize_class(jsonObj):
    serialized_nodes = [node.to_dict() for node in jsonObj.nodes()]
    # data["nodes"] = serialized_nodes
    return jsonObj

G = nx.Graph()
node1 = CustomNode("Node1", "Attribute1")
node2 = CustomNode("Node2", "Attribute2")
G.add_edge(node1, node2)


@router.get("/")
async def read_items():
    return "Hello World"


@router.get("/graphDemo")
def get_graph_demo():
    graph_data = serialize_graph(G)
    return JSONResponse(content=graph_data)


@router.get("/graph")
def get_graph():
    graph_data = sim_params()
    return JSONResponse(content=graph_data)

@router.get("/graphDev")
def get_graph():
    global simulation_thread, env
    if simulation_thread is not None:
        raise HTTPException(
            status_code=400, detail="Simulation already running")
    evaluation , res = run_sim(env)
    graph_data = serialize_graph(res)
    # graph_data = run_sim()
    return JSONResponse(content=graph_data)