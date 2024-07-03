"""Test code in the entrypoint file for the affils service."""

# In-house code:
from .app import app

# Configure app for testing.
app.config.update({"TESTING": True})

# Constants:
CLIENT = app.test_client()


def test_index_route():
    """Ensure index route redirects."""
    response = CLIENT.get("/")
    assert response.status_code == 200
    assert "<table>" in response.text
    assert "<th>ID</th>" in response.text
    assert "<td>10000</td>" in response.text
    assert "<th>Name</th>" in response.text
    assert "<td>Interface Admin</td>" in response.text


def test_login_route():
    """Ensure we see inputs for email and password."""
    response = CLIENT.get("/login")
    assert response.status_code == 200
    assert '<input id="email"' in response.text
    assert '<input id="password"' in response.text


def test_logout_route():
    """Ensure we redirect to the index."""
    response = CLIENT.get("/logout")
    assert response.status_code == 302


def test_signup_route():
    """Ensure we see instructions for signing up.

    Specifically, we hope to see a link to curation.clinicalgenome.org
    because we are using their user authentication service.
    """
    response = CLIENT.get("/signup")
    assert 'href="https://curation.clinicalgenome.org/"' in response.text


def test_sha_route():
    """Ensure we can get a Git SHA."""
    response = CLIENT.get("/sha")
    assert response.status_code == 200
    assert len(response.text) == 40  # SHA-1 is 40 characters in length.


def test_edit_route():
    """Ensure edit route redirects."""
    response = CLIENT.get("/edit?affil=10000")
    assert response.status_code == 200
    assert "Submit</button>" in response.text
    assert "<button>Cancel" in response.text
    assert "<label>Name:</label>" in response.text
    assert (
        '<input type="text" value="Interface Admin" placeholder="Name" />'
        in response.text
    )
    assert "<label>Family:</label>" in response.text
