from fastapi.testclient import TestClient

from ..main import app
import json
client = TestClient(app) 

def test_get_defaults(): 
    form_data = {
        "run": {
            "total_nodes": 100,
            "total_endpoints": 10,
            "total_layers": 4,
            "terminate_compromise_ratio": 0.9,
            "scheme": "simultaneous",
            "mtd_interval": 2,
            "finish_time": 9000,
            "checkpoints": 1000,
            "total_subnets": 6,
            "target_layer": None
        },
        "config": {
            "MTD_PRIORITY": {
                "CompleteTopologyShuffle": 7,
                "HostTopologyShuffle": 6,
                "IPShuffle": 5,
                "OSDiversity": 4,
                "PortShuffle": 1,
                "ServiceDiversity": 2,
                "UserShuffle": 3
            },
            "MTD_TRIGGER_INTERVAL": None
        }
    }
    response = client.post("network/update_all_params", json=form_data)

    assert response.status_code == 200

    response_json = response.json()["item"]
    from routers.network import stored_params
    assert "run" in response_json
    assert "config" in response_json
    config_response = client.get('/config/getCurrent')
    assert config_response.status_code == 200

    config_json = response.json()
    print(config_response)
