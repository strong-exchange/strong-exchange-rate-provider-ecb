from datetime import date

from fastapi.testclient import TestClient

from .main import app
from .data import rates
from .tasks import load_history_from_ecb_file

client = TestClient(app)


def test_empty_at_latest_rates_when_nothing_loaded():
    response = client.get("/latest")

    assert response.status_code == 200
    assert response.json()["base"] == "EUR"
    assert response.json()["rates"] == []
    assert response.json()["date"] is None


def test_appears_what_loaded_at_latest_rates():
    rates["USD"] = 1.0

    response = client.get("/latest")

    assert response.status_code == 200
    assert response.json()["base"] == "EUR"
    assert response.json()["rates"] == [{"currency": "USD", "rate": 1.0}]


def test_filter_by_symbol_at_latest_rates():
    rates["USD"] = 1.0
    rates["THB"] = 30.0

    response = client.get("/latest?symbols=USD")

    assert response.status_code == 200
    assert response.json()["base"] == "EUR"
    assert response.json()["rates"] == [{"currency": "USD", "rate": 1.0}]


def test_filter_by_symbols_at_latest_rates():
    rates["USD"] = 1.0
    rates["THB"] = 30.0
    rates["RUR"] = 70.0

    response = client.get("/latest?symbols=USD,RUR")

    assert response.status_code == 200
    assert response.json()["base"] == "EUR"
    assert response.json()["rates"] == [
        {"currency": "USD", "rate": 1.0},
        {"currency": "RUR", "rate": 70.0},
    ]


def test_if_history_not_loaded_interval_is_empty():
    response = client.get("/history?start_at=2024-04-01&end_at=2024-04-10")

    assert response.status_code == 200
    assert response.json()["start_at"] == "2024-04-01"
    assert response.json()["end_at"] == "2024-04-10"
    assert response.json()["rates"] == {}


def test_if_wrong_interval_returned_error():
    response = client.get("/history?start_at=2024-04-10&end_at=2024-04-01")

    assert response.status_code == 422
    assert response.json() == {"detail": "Wrong interval."}


def test_if_end_date_not_specified_it_will_be_6_days_after_start_date():
    response = client.get("/history?start_at=2024-04-01")

    assert response.status_code == 200
    assert response.json()["start_at"] == "2024-04-01"
    assert response.json()["end_at"] == "2024-04-07"


def test_if_start_date_is_not_specified_it_will_be_6_days_before_end_date():
    response = client.get("/history?end_at=2024-04-07")

    assert response.status_code == 200
    assert response.json()["start_at"] == "2024-04-01"
    assert response.json()["end_at"] == "2024-04-07"


def test_if_history_loaded_interval_is_not_empty():
    load_history_from_ecb_file()

    response = client.get("/history?start_at=2024-04-01&end_at=2024-04-10")

    assert response.status_code == 200
    assert response.json()["start_at"] == "2024-04-01"
    assert response.json()["end_at"] == "2024-04-10"
    assert response.json()["rates"] != {}
    assert len(response.json()["rates"].keys()) == 7
    assert len(response.json()["rates"]["2024-04-02"]) == 30


def test_can_filter_history_by_symbol():
    load_history_from_ecb_file()

    response = client.get("/history?symbols=USD&start_at=2024-04-01")

    assert response.status_code == 200
    assert len(response.json()["rates"]["2024-04-02"]) == 1


def test_history_works_without_intervals():
    response = client.get("/history?symbols=USD")

    assert response.status_code == 200
    assert response.json()["end_at"] == str(date.today())
