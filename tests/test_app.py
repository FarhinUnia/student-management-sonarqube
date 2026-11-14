
import pytest
from app import app, students


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_students(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_get_existing_student(client):
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "John Smith"


def test_get_missing_student(client):
    response = client.get("/students/999")
    assert response.status_code == 404


def test_add_student(client):
    new_student = {
        "name": "Michael Green",
        "email": "michael@gmail.com",
        "course": "Computer Science"
    }

    response = client.post("/students", json=new_student)

    assert response.status_code == 201
    assert response.get_json()["name"] == "Michael Green"


def test_delete_missing_student(client):
    response = client.delete("/students/999")
    assert response.status_code == 404

def test_add_student_with_empty_name(client):
    response = client.post("/students", json={
        "name": "",
        "email": "test@gmail.com",
        "course": "Computer Science"
    })

    assert response.status_code == 400


def test_update_student_with_empty_name(client):
    response = client.put("/students/1", json={
        "name": ""
    })

    assert response.status_code == 400


def test_update_student_with_invalid_json(client):
    response = client.put("/students/1", data="invalid", content_type="text/plain")

    assert response.status_code == 400