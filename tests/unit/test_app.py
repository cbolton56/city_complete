
import pytest
from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_client():
    """Test the client """
    response = client.get("/")
    assert response.status_code == 200

def test_get_suggestions():
    response = client.get("/suggestions?q=london&lat=31&long=42")
    assert response.status_code == 200
    print(response.text)

def test_get_suggestions_without_optional_params():
    response = client.get("/suggestions?q=london")
    assert response.status_code == 200
    print(response.text)
