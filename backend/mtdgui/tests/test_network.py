from fastapi.testclient import TestClient
from ..main import app
from routers.network import parameters
import json
client = TestClient(app) 

def test_make_new_default_graph(): 
    default_params = parameters
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
            "total_nodes": 40,
            "total_endpoints": 5,
            "total_layers": 3,
            "terminate_compromise_ratio": 0.7,
            "scheme": "random",
            "mtd_interval": 2.0,
            "finish_time": 8000,
            "checkpoints": 1000,
            "total_subnets": 3,
            "target_layer": 2
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

