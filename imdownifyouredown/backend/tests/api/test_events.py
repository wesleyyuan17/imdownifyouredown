import pytest

from fastapi.testclient import TestClient


def test_endpoint_basic(client: TestClient):
    response = client.get("/events/1")
    assert response.status_code == 200
    assert response.json() == [[1, 'test1', [1, 2, 3], 1]]
