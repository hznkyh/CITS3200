from typing import List
from fastapi.testclient import TestClient
from ..main import app
from ..routers.network import reset, stored_params
import networkx as nx
from ..models import NetworkGraph, NetworkGraphs
import json

client = TestClient(app)
# Define test data
headers: str = None
form_data = {
    "graph": {"graph_name": "1"},
    "run": {
        "total_nodes": 30,
        "total_endpoints": 5,
        "total_layers": 4,
        "terminate_compromise_ratio": 0.2,
        "scheme": "random",
        "mtd_interval": 2.0,
        "finish_time": 3000,
        "checkpoints": 1000,
        "total_subnets": 6,
        "target_layer": 4,
    },
    "config": None,
}
credentials = {
    "username": "da017b12-8470-47f4-a4e9-58182b6f3ee3",
    "password": "da017b12-8470-47f4-a4e9-58182b6f3ee3",
}




def test_update_run_parameters():
    # Step 1: Get the token

    token_response = client.post("/token/", data=credentials)

    assert token_response.status_code == 200
    token = token_response.json().get("access_token")

    global headers, form_data
    # Set up headers for authenticated request
    headers = {"Authorization": f"Bearer {token}"}

    # Step 2:  Send the request
    response = client.post("network/graph-params", json=form_data, headers=headers)

    assert response.status_code == 202
    assert response.json() == "prams set"


def test_make_new_default_graph():
    global headers, form_data
    graph_response = client.get("network/graph", headers=headers)
    
    name: str = list(graph_response.json().keys())[0]
    response_graph = NetworkGraphs(graphs=graph_response.json()[name])
    # graph_json
    assert name == form_data["graph"]["graph_name"]
    graph_list: List[nx.Graph] = [
        nx.node_link_graph(g) for g in graph_response.json()[name]
    ]

    assert response_graph.graphs.__len__() == (
        form_data["run"]["finish_time"] / form_data["run"]["checkpoints"]
    )

    for graph in graph_list:
        # Each checkpoint should return directed, multipgraph, graph, nodes and links
        # assert graph == 5
        # Check that each checkpoint has the right number of nodes
        assert len(graph.nodes) == form_data["run"]["total_nodes"]
        


def test_update_run_parameters_multi_graph():
    # Step 1: Get the token
    credentials = {
        "username": "da017b12-8470-47f4-a4e9-58182b6f3ee3",
        "password": "da017b12-8470-47f4-a4e9-58182b6f3ee3",
    }
    token_response = client.post("/token/", data=credentials)

    assert token_response.status_code == 200
    token = token_response.json().get("access_token")

    global headers, form_data
    # Set up headers for authenticated request
    headers = {"Authorization": f"Bearer {token}"}
    dict_form_data = {}
    
    for i in range(2):
        d = {
            "graph": {
                "graph_name" : str(i)
            }
        }
        dict_form_data[i] = form_data | d

    # # Step 2:  Send the request
    response = client.post("network/multi-graph-params", json=dict_form_data, headers=headers)

    assert response.status_code == 202
    assert response.json() == "prams set"


def test_make_new_default_multi_graph():
    global headers, form_data
    graph_response = client.get("network/multi-graph", headers=headers)
    
    assert graph_response.status_code == 200
    
    for name in graph_response.json().keys():
        response_graph = NetworkGraphs(graphs=graph_response.json()[name])
        # graph_json

        assert name in ['0', '1']
        graph_list: List[nx.Graph] = [
            nx.node_link_graph(g) for g in graph_response.json()[name]
        ]

        assert response_graph.graphs.__len__() == (
            form_data["run"]["finish_time"] / form_data["run"]["checkpoints"]
        )

        for graph in graph_list:
            # Each checkpoint should return directed, multipgraph, graph, nodes and links
            # Check that each checkpoint has the right number of nodes
            assert len(graph.nodes) == form_data["run"]["total_nodes"]
    

