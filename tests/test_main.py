import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API"}

def test_tasks_router_included():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json()["tasks"], list)

def test_invalid_route():
    response = client.get("/invalid")
    assert response.status_code == 404

def test_method_not_allowed():
    response = client.post("/")
    assert response.status_code == 405

@pytest.mark.parametrize("path", ["/tasks", "/tasks/"])
def test_tasks_router_prefix(path):
    response = client.get(path)
    assert response.status_code == 200
    assert isinstance(response.json()["tasks"], list)
