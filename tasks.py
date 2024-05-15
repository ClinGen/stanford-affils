"""Script for running any/all command line tasks for this project.

All command line tasks should be defined in this file. The only
exception to this is managing dependencies via Pipenv.
"""

# Third-party dependencies:
from dotenv import dotenv_values
from invoke import task

# Environment variable files:
ENV_TRUTH = ".env.template"  # The source of truth for all .env files.
ENV_LOCAL = ".env.local"
ENV_PROD = ".env.prod"

# Configs:
TRUTH_CONFIG = dotenv_values(ENV_TRUTH)
LOCAL_CONFIG = dotenv_values(ENV_LOCAL)
PROD_CONFIG = dotenv_values(ENV_PROD)
CONFIGS = [LOCAL_CONFIG, PROD_CONFIG]


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


@task
def envsame(c):
    """Ensure environment variable keys match in each .env file."""
    for config in CONFIGS:
        if config.keys() != TRUTH_CONFIG.keys():
            print(".env keys do not match. Check your .env files.")
            exit(1)


@task(pre=[fmt, lint, types, test, envsame])
def check(c):
    """Run all code checks."""


@task
def reqs(c):
    """Generate requirements.txt file.

    The GitHub Actions workflow runners don't seem to play nicely with
    Pipenv. We generate a requirements.txt file and use it to install
    dependencies in GitHub Actions.

    We also use the requirements.txt file on Elastic Beanstalk.
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
    c.run(f"source {ENV_LOCAL} && cd src && flask run")
