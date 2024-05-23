from fastapi.testclient import TestClient

from .main import app
from .data import rates

client = TestClient(app)



def test_empty_at_latest_rates_when_nothing_loaded():
    response = client.get('/latest')

    assert response.status_code == 200
    assert response.json()['base'] == 'EUR'
    assert response.json()['rates'] == []
    assert response.json()['date'] is None



def test_appears_what_loaded_at_latest_rates():
    rates['USD'] = 1.0

    response = client.get('/latest')

    assert response.status_code == 200
    assert response.json()['base'] == 'EUR'
    assert response.json()['rates'] == [
        {'currency': 'USD', 'rate': 1.0}
    ]
