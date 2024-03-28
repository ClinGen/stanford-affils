"""Entrypoint file for the affils service.

Set up API routes.
"""

# Built-in libraries:
import logging
import os
import subprocess

# Third-party dependencies:
from flask import Flask

# Configure logger.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def hello_world():
    """A cheeky hello world route."""
    logger.info("User accessed /")
    return "<p>Look on my Affiliations Service, ye Mighty, and despair!</p>"


@app.route("/sha")
def current_git_sha():
    """Displays current Git SHA."""
    logger.info("User accessed /sha")
    command = ["git", "rev-parse", "HEAD"]
    output = subprocess.run(command, check=False, capture_output=True).stdout.decode(
        "utf-8"
    )
    # Strip newline character from the end of the string.
    sha = output[0 : len(output) - 1]
    return sha


@app.route("/env")
def display_env_var():
    """Displays environment variable for testing purposes."""
    logger.info("User accessed /env")
    return os.environ.get("SOME_VAR")
