from fastapi.testclient import TestClient

from . import app #type: ignore

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    print(response)
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}
