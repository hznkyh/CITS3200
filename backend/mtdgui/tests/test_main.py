from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app) 
#Todo finish test
def test_make_new_default_graph(): 
    response = client.get('/network/testGraph')