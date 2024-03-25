"""Script for running any/all command line tasks for this project.

All command line tasks should be defined in this file. The only
exception to this is managing dependencies via Pipenv.
"""

# Third-party dependencies:
from invoke import task


@task
def fmt(c):
    """Format code."""
    c.run(f"black .")


@task
def lint(c):
    """Run the linter."""
    c.run(f"pylint src")


@task
def types(c):
    """Check types."""
    c.run("mypy .")


@task
def test(c):
    """Run the test suite."""
    c.run("coverage run -m pytest && coverage report")


@task(pre=[fmt, lint, types, test])
def check(c):
    """Run all code checks."""


@task
def reqs(c):
    """Generate requirements.txt file for use in GitHub Actions.

    The GitHub Actions workflow runners don't seem to play nicely with
    Pipenv. We generate a requirements.txt file and use it to install
    dependencies in GitHub Actions.
    """
    add_warning = (
        "echo '# Do not edit directly. This file is generated.\n' > requirements.txt"
    )
    # The PIPENV_VERBOSITY variable suppresses a warning issued Pipenv
    # if you use the run command when you've already activated the
    # virtual environment.
    add_reqs = "PIPENV_VERBOSITY=-1 pipenv run pip freeze >> requirements.txt"
    c.run(f"{add_warning} && {add_reqs}")


@task
def dev(c):
    """Run the development server.

    Assumes you've activated the virtual environment.
    """
    c.run("cd src && flask run")


@task
def deploy(c):
    """Deploy the affils service.

    Assumes you have the Elastic Beanstalk CLI tool, eb. Also assumes
    you have AWS configured properly. You should set Oregon (us-west-2)
    as your AWS region, and you should have AWS production credentials.
    """
    c.run("eb deploy")
