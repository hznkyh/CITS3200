from fastapi.testclient import TestClient
from ..main import app
import json
client = TestClient(app) 

def test_make_new_default_graph(): 
    response = client.get('/network/graph')
    assert response.status_code == 200 
    data = response.json()
    assert len(data) == 3
  