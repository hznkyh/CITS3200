from fastapi.testclient import TestClient
from ..main import app
from routers.network import parameters,reset
import json
client = TestClient(app) 

def test_make_new_default_graph(): 
    default_params = parameters
    reset()
    response = client.get('/network/graph')
    assert response.status_code == 200 
    data = response.json()
    # Should be 10 checkpoints in the default response 
    assert len(data) == len(parameters["checkpoints"])
    # Each checkpoint should return directed, multipgraph, graph, nodes and links
    for i in range(0,len(data)): 
        assert len(data[str(i)]) == 5
        # Check that each checkpoint has the right number of nodes
        assert len(data[str(i)]["nodes"]) == parameters["total_nodes"]

def test_update_run_parameters(): 
    # Define test data
    form_data = {
        "run": {
            "total_nodes": 100,
            "total_endpoints": 10,
            "total_layers": 4,
            "terminate_compromise_ratio": 0.7,
            "scheme": "random",
            "mtd_interval": 2.0,
            "finish_time": 9000,
            "checkpoints": 1000,
            "total_subnets": 4,
            "target_layer": 4
        },
        "config": None
    }
    response = client.post("network/update_all_params", json=form_data)

    assert response.status_code == 200

    response_json = response.json()["item"]
    from routers.network import stored_params
    assert "run" in response_json
    assert "config" in response_json

    for key in form_data["run"]:
        assert form_data["run"][key] == stored_params[key]


    graph_response = client.get("network/graph")

    graph_json = graph_response.json()
    final_params = parameters | stored_params
    if type(final_params["checkpoints"]) is int: 
        final_params["checkpoints"] =  range(final_params["start_time"], int(final_params["finish_time"]), final_params["checkpoints"])
    print(graph_json)
    assert len(graph_json) == len(final_params["checkpoints"])
    for i in range(0,len(graph_json)): 
        # Each checkpoint should return directed, multipgraph, graph, nodes and links
        assert len(graph_json[str(i)]) == 5
        # Check that each checkpoint has the right number of nodes
        assert len(graph_json[str(i)]["nodes"]) == final_params["total_nodes"]
    