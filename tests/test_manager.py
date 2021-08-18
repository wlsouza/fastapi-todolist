import pytest
from fastapi.testclient import TestClient
from fastapi import status

from task_manager.manager import app, TASKS

@pytest.fixture(name="client")
def get_client():
    return TestClient(app)


@pytest.fixture
def init_tasks_list():
    TASKS.clear()
    TASKS.append({
        "id": 1,
        "title": "Take a shower",
        "description": "Take a shower to go to work.",
        "state": "not-done",
    })
    yield TASKS
    #teardown
    TASKS.clear()



def test_when_listing_tasks_returns_status_200(client):
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK

def test_when_listing_tasks_returns_a_json_contenttype(client):
    response = client.get("/tasks")
    assert response.headers["Content-Type"] == "application/json"

def test_when_listing_tasks_returns_a_list(client):
    response = client.get("/tasks")
    assert isinstance(response.json(), list)

def test_when_listing_tasks_the_returned_tasks_must_have_id(client, init_tasks_list):
    # TASKS.append({"id": 1})
    response = client.get("/tasks")
    assert "id" in response.json().pop()
    # TASKS.clear()

def test_when_listing_tasks_the_returned_tasks_must_have_title(client, init_tasks_list):
    # TASKS.append({"title": "This is a title"})
    response = client.get("/tasks")
    assert "title" in response.json().pop()
    # TASKS.clear()

def test_when_listing_tasks_the_returned_tasks_must_have_description(client, init_tasks_list):
    # TASKS.append({"description": "This is a valid description"})
    response = client.get("/tasks")
    assert "description" in response.json().pop()
    # TASKS.clear()

def test_when_listing_tasks_the_returned_tasks_must_have_state(client, init_tasks_list):
    # TASKS.append({"state": "done"})
    response = client.get("/tasks")
    assert "state" in response.json().pop()
    # TASKS.clear()