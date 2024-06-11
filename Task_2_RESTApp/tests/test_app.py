
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_data(client):
    response = client.get('/getdata?type=sports')
    assert response.status_code == 200

def test_get_data_invalid_type(client):
    response = client.get('/getdata?type=invalid_type')
    assert response.status_code == 400

def test_get_data_by_slug_sports(client):
    response = client.get('/sports/football')
    assert response.status_code == 200

def test_get_data_by_slug_events(client):
    response = client.get('/events/ipl-final')
    assert response.status_code == 200

def test_get_data_by_slug_invalid_type(client):
    response = client.get('/invalid_type/slug')
    assert response.status_code == 400

def test_create_data_sports(client):
    data = {
        "entity_type": "sports",
        "name": "test_sport",
        "slug": "test_sport_create",
        "active": 1
    }
    response = client.post('/create', json=data)
    assert response.status_code == 201

def test_create_data_invalid_type(client):
    data = {
        "entity_type": "invalid_type",
        "name": "Test",
        "slug": "test",
        "active": 1
    }
    response = client.post('/create', json=data)
    assert response.status_code == 400

def test_update_data_sports(client):
    data = {
        "name": "Updated Name",
        "slug": "updated-slug",
        "active": 0
    }
    response = client.put('/update/sports/9', json=data)
    assert response.status_code == 200

    # Close the database connection after the test
    # app.db_connection.close()

def test_update_data_invalid_type(client):
    data = {
        "name": "Updated Name",
        "slug": "updated-slug",
        "active": 0
    }
    response = client.put('/update/invalid_type/1', json=data)
    assert response.status_code == 400
