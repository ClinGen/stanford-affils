"""Test code in the entrypoint file for the affils service."""

# In-house code:
from .app import app

# Configure app for testing.
app.config.update({"TESTING": True})

# Constants:
CLIENT = app.test_client()


def test_root():
    """Ensure our cheeky hello world route works."""
    response = CLIENT.get("/")
    assert response.status_code == 200
    assert response.json == {
        "message": "Look on my Affiliations Service, ye Mighty, and despair!"
    }
