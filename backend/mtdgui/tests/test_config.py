from fastapi.testclient import TestClient
from ..main import app
from routers import develop,network,config
import json
client = TestClient(app) 

def test_get_defaults(): 
    response = client.get('/config/getCurrent')
    assert response.status_code == 200

    config_response = response.json()
    print(config_response)
