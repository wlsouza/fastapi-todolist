import pytest

from fastapi.testclient import TestClient
from fastapi import status

from pydantic import UUID4

from task_manager.manager import app, TASKS

@pytest.fixture(name="client")
def get_client():
    return TestClient(app)


@pytest.fixture
def init_tasks_list():
    TASKS.clear()
    TASKS.append(
        {
            "id": UUID4("020f5896-4bfa-4017-8d83-19a6eb489895"),
            "title": "Take a shower",
            "description": "Take a shower to go to work.",
            "state": "not-done"
        }
    )
    yield TASKS
    #teardown
    TASKS.clear()




#region testing "/tasks" (GET)
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
    response = client.get("/tasks")
    assert "id" in response.json().pop()

def test_when_listing_tasks_the_returned_tasks_must_have_title(client, init_tasks_list):
    response = client.get("/tasks")
    assert "title" in response.json().pop()

def test_when_listing_tasks_the_returned_tasks_must_have_description(client, init_tasks_list):
    response = client.get("/tasks")
    assert "description" in response.json().pop()

def test_when_listing_tasks_the_returned_tasks_must_have_state(client, init_tasks_list):
    response = client.get("/tasks")
    assert "state" in response.json().pop()

def test_when_listing_tasks_the_returned_tasks_must_be_ordered_by_state_not_done_first(client, init_tasks_list):
    expected = [
        {
        "id": "020f5896-4bfa-4017-8d83-19a6eb489895",
        "title": "Take a shower",
        "description": "Take a shower to go to work.",
        "state": "not-done"
        },{
        "id": "11455eca-8f56-403b-a257-485ee61a2d80",
        "title": "Fuel the car",
        "description": "fuel the car because it is out of gas.",
        "state": "done",
        }
    ]
    TASKS.clear()
    TASKS.extend(expected[::-1])
    response = client.get("/tasks")
    assert response.json() == expected

#endregion

#region testing "/tasks" (POST)
def test_resource_tasks_must_accept_post_verb(client):
    response = client.post("/tasks")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

def test_when_create_tasks_if_the_request_payload_doesnt_have_title_return_422(client):
    payload = {
        "description": "Take a shower to go to work.",
        "state": "not-done"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_when_create_tasks_the_title_must_have_more_than_2_characters(client):
    payload = {
        "title": "AA",
        "description": "Take a shower to go to work.",
        "state": "not-done"
    }
    response = client.post("/tasks",json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_when_create_tasks_the_title_must_have_less_than_51_characters(client):
    payload = {
        "title": "A"*55,
        "description": "Take a shower to go to work.",
        "state": "not-done"
    }
    response = client.post("/tasks",json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_when_create_tasks_if_the_request_payload_doesnt_have_description_return_422(client):
    payload = {
        "Title": "Testing",
        "state": "not-done"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_when_create_tasks_the_description_must_have_less_than_141_characters(client):
    payload = {
        "title": "Testing",
        "description": "A"*141,
        "state": "not-done"
    }
    response = client.post("/tasks",json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_when_create_task_it_must_be_returned(client):
    payload = {
        "title": "Testing",
        "description": "Testing the API",
        "state": "not-done"
    }
    response = client.post("/tasks",json=payload)
    assert payload.items() <= response.json().items() # the payload.items() is subset (it's contained) of response.json().items()

def test_when_create_task_the_task_id_must_be_unique(client):
    payload = {
        "title": "Testing",
        "description": "Testing the API",
        "state": "not-done"
    }
    response1 = client.post("/tasks", json=payload)
    response2 = client.post("/tasks", json=payload)
    assert response1.json()["id"] != response2.json()["id"]

def test_when_create_task_the_default_state_must_be_not_done(client):
    payload = {
        "title": "Testing",
        "description": "Testing the API"
    }
    response = client.post("/tasks", json=payload)
    assert response.json()["state"] == "not-done"

def test_when_create_a_task_with_success_the_status_must_be_201(client):
    payload = {
        "title": "Testing",
        "description": "Testing the API",
        "state": "not-done"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

def test_when_create_task_it_must_be_persisted(client):
    number_tasks_before = len(TASKS)
    payload = {
        "title": "Testing",
        "description": "Testing the API",
        "state": "done"
    }
    response = client.post("/tasks", json = payload)
    # The code bellow was commented to maintain the test independent 
    # response2 = client.get("/tasks", json = payload)
    # assert any(response.json().items() <= task.items() for task in response2.json()) 
    assert len(TASKS) == number_tasks_before+1

#endregion

#region testing "/tasks/{id}" (DELETE)
def test_resource_task_must_receive_delete_verb(client):
    response = client.delete("/tasks/58a7a73a-0055-4b9e-bbe9-9e1c1cbc4f88")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

def test_when_delete_a_task_if_its_not_found_returns_404(client, init_tasks_list):
    response = client.delete("/tasks/58a7a73a-0055-4b9e-bbe9-9e1c1cbc4f88")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_when_delete_the_task_successfully_returns_204(client, init_tasks_list):
    response = client.delete("/tasks/020f5896-4bfa-4017-8d83-19a6eb489895")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_when_delete_a_task_it_must_be_removed_from_tasks_repository(client, init_tasks_list):
    number_tasks_before = len(TASKS)
    client.delete("/tasks/020f5896-4bfa-4017-8d83-19a6eb489895")
    assert len(TASKS) == number_tasks_before -1

#endregion

#region testing "/tasks/{id}" (PUT)
def test_resource_task_must_receive_put_verb(client, init_tasks_list):
    response = client.put("/tasks/58a7a73a-0055-4b9e-bbe9-9e1c1cbc4f88")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

def test_when_updating_a_task_if_its_not_found_returns_404(client, init_tasks_list):
    payload = {
        "title": "Take a shower",
        "description": "Take a shower to go to work.",
        "state": "not-done"
    }
    response = client.put("/tasks/58a7a73a-0055-4b9e-bbe9-9e1c1cbc4f88", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_when_update_a_task_successfully_return_200(client, init_tasks_list):
    payload = {
        "title": "Take a shower",
        "description": "Take a shower to go to work.",
        "state": "done"
    }
    response = client.put("/tasks/020f5896-4bfa-4017-8d83-19a6eb489895", json=payload)
    assert response.status_code == status.HTTP_200_OK

def test_when_updating_task_if_the_received_payload_not_countain_all_necessary_task_data_must_return_422(client, init_tasks_list):
    payload = {
        "description": "Take a shower to go to work.",
        "state": "not-done"
    }
    response = client.put("/tasks/020f5896-4bfa-4017-8d83-19a6eb489895", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

def test_when_update_task_the_new_representation_of_that_must_be_returned(client, init_tasks_list):
    payload = {
        "title": "Take a shower",
        "description": "Take a shower to go to work.",
        "state": "done"
    }
    expected = {"id": "020f5896-4bfa-4017-8d83-19a6eb489895", **payload}
    response = client.put("/tasks/020f5896-4bfa-4017-8d83-19a6eb489895", json=payload)
    assert response.json() == expected


def test_when_update_a_task_the_alterations_must_be_persisted(client, init_tasks_list):
    payload = {
        "title": "Take a shower",
        "description": "Take a shower to go to work.",
        "state": "done"
    }
    expected = {"id": UUID4("020f5896-4bfa-4017-8d83-19a6eb489895"), **payload}
    response = client.put("/tasks/020f5896-4bfa-4017-8d83-19a6eb489895", json=payload)
    assert TASKS[0] == expected

def test_when_update_a_task_the_title_must_have_more_than_2_characters(client, init_tasks_list):
    payload = {
        "title": "AA",
        "description": "Take a shower to go to work.",
        "state": "done"
    }
    response = client.put("/tasks/020f5896-4bfa-4017-8d83-19a6eb489895", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_when_update_a_task_the_title_must_have_less_than_51_characters(client, init_tasks_list):
    payload = {
        "title": "A"*51,
        "description": "Take a shower to go to work.",
        "state": "done"
    }
    response = client.put("/tasks/020f5896-4bfa-4017-8d83-19a6eb489895", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_when_update_a_task_the_description_must_have_less_than_141_characters(client, init_tasks_list):
    payload = {
        "title": "Take a shower",
        "description": "A"*141,
        "state": "done"
    }
    response = client.put("/tasks/020f5896-4bfa-4017-8d83-19a6eb489895", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

#endregion