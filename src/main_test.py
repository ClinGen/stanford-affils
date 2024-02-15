"""Test code in the entrypoint file for the affils service."""

# Third-party dependencies:
from fastapi.testclient import TestClient

# In-house code:
from .main import app

client = TestClient(app)


def test_main():
    """Ensure our cheeky hello world route works."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Look on my Affiliations Service, ye Mighty, and despair!"
    }
