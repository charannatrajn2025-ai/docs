import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello from Flask DevOps Pipeline!' in response.data

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_data(client):
    response = client.get('/api/data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['count'] == 5