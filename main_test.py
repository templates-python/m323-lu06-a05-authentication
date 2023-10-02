import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_todo(client):
    response = client.post('/todos', json={"title": "Test Todo", "is_completed": False})
    assert response.status_code == 201

def test_get_all_todos(client):
    response = client.get('/todos')
    assert response.status_code == 200

def test_get_specific_todo(client):
    response = client.get('/todos/1')
    if response.status_code != 404:
        assert response.status_code == 200

def test_update_todo(client):
    response = client.put('/todos/1', json={"title": "Updated Test Todo", "is_completed": True})
    if response.status_code != 404:
        assert response.status_code == 200

def test_delete_todo(client):
    response = client.delete('/todos/1')
    if response.status_code != 404:
        assert response.status_code == 200