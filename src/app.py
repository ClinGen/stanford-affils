"""Entrypoint file for the affils service.

Set up API routes.
"""

# Built-in libraries:
import os
import subprocess
import sys

# Third-party dependencies:
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# In-house code:
from . import logger
from .affiliation import Affiliation
from .user import User

app = Flask(__name__)
if "AFFILS_FLASK_SECRET_KEY" in os.environ:
    app.secret_key = os.environ.get("AFFILS_FLASK_SECRET_KEY")
else:
    logger.error("Unable to find secret key; check your .env file")
    sys.exit(1)


@app.route("/")
def index():
    """The affiliations home page."""
    logger.info("User accessed /")
    # A note on cookie-based sessions: Flask will take the values you
    # put into the session object and serialize them into a cookie. If
    # you are finding some values do not persist across requests,
    # cookies are indeed enabled, and you are not getting a clear error
    # message, check the size of the cookie in your page responses
    # compared to the size supported by web browsers.
    email = session["email"] if "email" in session else None
    affiliations_set = Affiliation.all()
    return render_template("index.html", affiliations=affiliations_set, email=email)


@app.route("/edit")
def edit():
    """The edit route.

    Edit an existing affiliation.
    """
    logger.info("User accessed edit")
    affil_id = request.args.get('affil')
    if not affil_id:
        return redirect(url_for("index"))
    email = session["email"] if "email" in session else None
    # TODO(sanchegm): Redirect to main page if user is not logged in.
    affiliation = Affiliation.get_by_id(affil_id)
    if not affiliation:
        return redirect(url_for("index"))
    return render_template("edit.html", affiliation=affiliation, email=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    """The login route.

    Either redirect a logged-in user to the home page or show the user
    a login form.
    """
    logger.info("User accessed /login")
    if request.method == "POST":
        user = User(request.form["email"], request.form["password"])
        user.login()
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log the user out."""
    logger.info("User accessed /logout")
    session.pop("email", None)
    return redirect(url_for("index"))


@app.route("/signup")
def signup():
    """Show the user sign-up instructions."""
    logger.info("User accessed /signup")
    return render_template("signup.html")


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
