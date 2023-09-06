import json
import threading
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
n_directory = os.path.join(Path(__file__).parents[2])
# Add the "s" directory to the Python path
sys.path.append(n_directory)
print("N")
print(n_directory)
print("N")
from run import get_sim_json
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
        "nodes": [serialize_class(G,n,name)  for n in G],
        # "nodes": [dict(chain(G.nodes[n].items(), [(name, n)])) for n in G],
    }
        
    if multigraph:
        data[links] = [
            dict(chain(d.items(), [(source, u), (target, v), (key, k)]))
            for u, v, k, d in G.edges(keys=True, data=True)
        ]
    else:            
        data[links] = [
            dict(chain(d.items(), [(source, u), (target, v)]))
            for u, v, d in G.edges(data=True)
        ]
    return data
    # return data

def serialize_class(G,n,name):
    node = dict(chain(G.nodes[n].items(), [(name, n)]))
    node['host'] = node['host'].toJson()
    return node


@router.get("/")
async def read_items():
    return "Hello World"

@router.get("/graph")
async def get_graph():
    global simulation_thread, env
    if simulation_thread is not None:
        simulation_thread.join()
        raise HTTPException(
            status_code=400, detail="Simulation already running")
    
    print('init',env)
    evaluation , res = create_sim(env, start_time=0, finish_time= 4, new_network=True)
    simulation_thread = threading.Thread(target=env.run, args=(([2])))
    simulation_thread.start()
    simulation_thread.join()
    graph_data = serialize_graph(evaluation.get_network().graph)
    return JSONResponse(content=graph_data)
    
@router.get("/graphDevEnd")
async def get_graph():
    global simulation_thread, env
    if simulation_thread is None:
        raise HTTPException(status_code=400, detail=f"No simulation running and is alive : {simulation_thread.is_alive()}")
    env.timeout(0)
    simulation_thread.join()
    simulation_thread = None
    env = simpy.Environment()  # create a new environment
    return JSONResponse(content="Simulation stopped", status_code=400)
    
@router.get("/testGraph")
async def get_sim():
    return get_sim_json()
get_sim_json()
# get_graph()