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
def dev(c):
    """Run the development server.

    Assumes you've activated the virtual environment.
    """
    c.run("cd src && uvicorn main:app --reload")
