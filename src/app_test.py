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
    assert (
        response.text
        == "<p>Look on my Affiliations Service, ye Mighty, and despair!</p>"
    )


def test_sha():
    """Ensure we can get a SHA."""
    response = CLIENT.get("/sha")
    assert response.status_code == 200
    assert len(response.text) == 40  # SHA-1 is 40 characters in length.
