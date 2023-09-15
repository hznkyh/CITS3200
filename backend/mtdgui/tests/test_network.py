from fastapi.testclient import TestClient
from ..main import app
import json
client = TestClient(app) 

def test_make_new_default_graph(): 
    response = client.get('/network/graph')
    assert response.status_code == 200 
    data = response.json()
    assert len(data) == 3

def test_update_run_parameters(): 
    # Define test data
    form_data = {
        "total_nodes": 30,
        "total_endpoints": 5,
        "total_layers": 3,
        "terminate_compromise_ratio": 0.7,
        "scheme": "random",
        "mtd_interval": 2.0,
        "finish_time": 9000,
        "checkpoints": 1000,
        "total_subnets": 2,
        "target_layers": 4,
        "MTD_PRIORITY": None,
        "MTD_TRIGGER_INTERVAL": None
    }

    response = client.post("/update_submit/", json=form_data)

    assert response.status_code == 200

    response_json = response.json()
    assert "form_data" in response_json
    assert "MTD_PRIORITY" in response_json
    assert "MTD_TRIGGER_INTERVAL" in response_json

    assert response_json['form_data'] == form_data
    assert response_json['MTD_PRIORITY'] == form_data['MTD_PRIORITY']
    assert response_json['MTD_TRIGGER_INTERVAL'] == form_data['MTD_TRIGGER_INTERVAL']

    graph_response = client.get("/network/graph")

    
