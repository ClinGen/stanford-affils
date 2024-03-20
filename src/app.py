"""Entrypoint file for the affils service.

Set up API routes.
"""

# Third-party dependencies:
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    """A cheeky hello world route."""
    return {"message": "Look on my Affiliations Service, ye Mighty, and despair!"}
