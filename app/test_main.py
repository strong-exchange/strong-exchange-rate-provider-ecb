from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)



def test_can_get_latest_rates():
    response = client.get('/latest')
    assert response.status_code == 200
    assert response.json() == {
        'base': 'EUR',
        'rates': {
            'USD': 1.1
        }
    }
