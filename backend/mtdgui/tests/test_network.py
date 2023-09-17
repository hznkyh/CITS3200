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
        "run":
        { 
            "total_nodes": 30,
            "total_endpoints": 5,
            "total_layers": 3,
            "terminate_compromise_ratio": 0.7,
            "scheme": "random",
            "mtd_interval": 2.0,
            "finish_time": 9000,
            "checkpoints": 1000,
            "total_subnets": 2,
            "target_layers": 4  
        },
        "config":
        { 
            "MTD_TRIGGER_INTERVAL": {
                "simultaneous": [700, 0.5],
                "random": [200, 0.5],
                "alternative": [200, 0.5]
            },
            "MTD_PRIORITY": {
                "CompleteTopologyShuffle": 1,
                "HostTopologyShuffle": 2,
                "IPShuffle": 3,
                "OSDiversity": 4,
                "PortShuffle": 5,
                "ServiceDiversity": 6,
                "UserShuffle": 7
            },
        }
    }

    response = client.post("network/update_submit/", json=form_data)

    assert response.status_code == 200

    response_json = response.json()
    assert "form_data" in response_json
    assert "MTD_PRIORITY" in response_json
    assert "MTD_TRIGGER_INTERVAL" in response_json

    config_response = client.get("/config/getCurrent")

    assert config_response.status_code == 200 
    # graph_response = client.get("network/graph")

    # assert graph_response.status_code == 200

    
