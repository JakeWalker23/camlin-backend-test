import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_wallet_endpoint_structure():
    response = client.get("/wallet")
    assert response.status_code == 200

    data = response.json()
    assert "holdings" in data
    assert "pln_holdings" in data
    assert "total_pln" in data

    assert isinstance(data["holdings"], dict)
    assert isinstance(data["pln_holdings"], dict)
    assert isinstance(data["total_pln"], (int, float))

def test_wallet_contains_pln_and_usd():
    response = client.get("/wallet")
    data = response.json()

    assert "PLN" in data["holdings"]
    assert "USD" in data["holdings"]
    assert data["pln_holdings"]["PLN"] == data["holdings"]["PLN"]