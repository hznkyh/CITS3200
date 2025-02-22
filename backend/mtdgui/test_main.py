from fastapi.testclient import TestClient

from . import app #type: ignore

client = TestClient(app)


def test_read_main():
    response = client.get("/")

    assert response.status_code == 200
