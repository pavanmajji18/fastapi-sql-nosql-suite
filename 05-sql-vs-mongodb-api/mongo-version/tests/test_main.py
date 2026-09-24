import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from app.main import app
from app.database import get_db

@pytest.fixture
def mock_db():
    client = AsyncMongoMockClient()
    return client["test_db"]

@pytest.fixture
def client(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_create_project(client):
    response = client.post("/projects", json={"title": "Test Project", "description": "A test project"})
    assert response.status_code == 201
    data = response.json()
    assert "_id" in data
    assert data["title"] == "Test Project"
    assert data["description"] == "A test project"

def test_create_task_and_get(client):
    # First create a project
    proj_resp = client.post("/projects", json={"title": "Main Project"})
    project_id = proj_resp.json()["_id"]

    # Create task for this project
    task_resp = client.post("/tasks", json={
        "title": "Build API",
        "description": "Implement endpoints",
        "project_id": project_id,
        "assignee_name": "Alice"
    })
    assert task_resp.status_code == 201
    task_data = task_resp.json()
    assert task_data["status"] == "TODO"
    task_id = task_data["_id"]

    # Update assignee
    assign_resp = client.patch(f"/tasks/{task_id}/assign", json={"assignee_name": "Bob"})
    assert assign_resp.status_code == 200
    assert assign_resp.json()["assignee_name"] == "Bob"

    # Update status
    status_resp = client.patch(f"/tasks/{task_id}/status", json={"status": "IN_PROGRESS"})
    assert status_resp.status_code == 200
    assert status_resp.json()["status"] == "IN_PROGRESS"

    # Get tasks filtered by project_id and status
    list_resp = client.get(f"/tasks?project_id={project_id}&status=IN_PROGRESS")
    assert list_resp.status_code == 200
    tasks = list_resp.json()
    assert len(tasks) == 1
    assert tasks[0]["_id"] == task_id

    # Delete task
    del_resp = client.delete(f"/tasks/{task_id}")
    assert del_resp.status_code == 204

    # Verify task deleted
    list_after_del = client.get(f"/tasks?project_id={project_id}")
    assert len(list_after_del.json()) == 0

def test_create_task_invalid_project(client):
    # Invalid ObjectId format
    resp = client.post("/tasks", json={"title": "Task", "project_id": "invalid_id"})
    assert resp.status_code == 400

    # Non-existent ObjectId
    resp2 = client.post("/tasks", json={"title": "Task", "project_id": "507f1f77bcf86cd799439011"})
    assert resp2.status_code == 404

def test_mongo_timeout_handler():
    from unittest.mock import MagicMock
    from pymongo.errors import ServerSelectionTimeoutError
    mock_failing_db = MagicMock()
    mock_failing_db.__getitem__.side_effect = ServerSelectionTimeoutError("Timeout")
    
    app.dependency_overrides[get_db] = lambda: mock_failing_db
    with TestClient(app) as test_client:
        resp = test_client.post("/projects", json={"title": "Fail Project"})
        assert resp.status_code == 503
        assert "Could not connect to MongoDB Atlas" in resp.json()["detail"]
    app.dependency_overrides.clear()

