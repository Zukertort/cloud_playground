from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Sanity Check: Does the app accept requests?
    """
    response = client.get("/")
    assert response.status_code == 200