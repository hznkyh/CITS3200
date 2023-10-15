from fastapi.testclient import TestClient

from ..main import app
import json

client = TestClient(app)

# def test_get_defaults():
#     form_data = {
#         "run": {
#             "total_nodes": 100,
#             "total_endpoints": 10,
#             "total_layers": 4,
#             "terminate_compromise_ratio": 0.9,
#             "scheme": "simultaneous",
#             "mtd_interval": 2,
#             "finish_time": 9000,
#             "checkpoints": 1000,
#             "total_subnets": 6,
#             "target_layer": None
#         },
#         "config": {
#             "MTD_PRIORITY": {
#                 "CompleteTopologyShuffle": 7,
#                 "HostTopologyShuffle": 6,
#                 "IPShuffle": 5,
#                 "OSDiversity": 4,
#                 "PortShuffle": 1,
#                 "ServiceDiversity": 2,
#                 "UserShuffle": 3
#             },
#             "MTD_TRIGGER_INTERVAL": None
#         }
#     }
#     response = client.post("network/update_all_params", json=form_data)

#     assert response.status_code == 200

#     response_json = response.json()["item"]
#     from routers.network import stored_params
#     assert "run" in response_json
#     assert "config" in response_json
#     config_response = client.get('/config/getCurrent')
#     assert config_response.status_code == 200

#     config_json = response.json()



def test_get_defaults():
    # Step 1: Get the token
    credentials = {
        "username": "da017b12-8470-47f4-a4e9-58182b6f3ee3",
        "password": "da017b12-8470-47f4-a4e9-58182b6f3ee3",
    }
    token_response = client.post("/token/", data=credentials)

    assert token_response.status_code == 200
    token = token_response.json().get("access_token")

    # Set up headers for authenticated request
    headers = {"Authorization": f"Bearer {token}"}

    # Your original test data
    form_data = {
        "additionalProp1": {
            "graph": {"graph_name": "G1"},
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
                "target_layer": None,
            },
            "config": None,
        }
    }

    # Step 2: Post with the token in the headers
    response = client.post(
        "network/multi-graph-params", json=form_data, headers=headers
    )

    assert response.status_code == 202


def test_get_defaults_with_config():
    # Step 1: Get the token
    credentials = {"username": "da017b12-8470-47f4-a4e9-58182b6f3ee3", "password": "da017b12-8470-47f4-a4e9-58182b6f3ee3"}
    token_response = client.post("/token/", data=credentials)

    assert token_response.status_code == 200
    token = token_response.json().get("access_token")

    # Set up headers for authenticated request
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Your original test data
    form_data = {
        "additionalProp1": {
            "graph": {"graph_name": "G1"},
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
                "target_layer": None,
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
    }


    # Step 2: Post with the token in the headers
    response = client.post("network/multi-graph-params", json=form_data, headers=headers)
    
    assert response.status_code == 202