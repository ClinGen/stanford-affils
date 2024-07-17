"""Script for common command line tasks for this project."""

import os

# Invoke always requires a context parameter, even if it ends up going
# unused. As of this writing, there are a handful of tasks that don't
# use their context parameters.
# pylint: disable=unused-argument

# Built-in libraries:
import sys

# Third-party dependencies:
from dotenv import dotenv_values
from dotenv import load_dotenv
from invoke import task

# Set environment variables.
load_dotenv()

# Environment variable files:
ENV_TEMPLATE = ".env.template"
ENV_ACTUAL = ".env"

# Configs:
TEMPLATE_CONF = dotenv_values(ENV_TEMPLATE)
ACTUAL_CONF = dotenv_values(ENV_ACTUAL)


@task
def fmt(c):
    """Format code."""
    c.run("black .")
    c.run("mdformat README.md")
    c.run("mdformat doc")


@task
def lint(c):
    """Run the linter."""
    c.run("pylint src")
    c.run("pylint tasks.py")


@task
def types(c):
    """Check types."""
    c.run("mypy .")


@task
def envsame(c):
    """Ensure environment variable keys match."""
    if TEMPLATE_CONF.keys() != ACTUAL_CONF.keys():
        print(".env keys do not match. Check your .env files.")
        sys.exit(1)


@task
def test(c):
    """Run test suite."""
    c.run(f"cd {os.getenv('AFFILS_WORKING_DIR')}/src && python manage.py test")


@task(pre=[fmt, lint, types, envsame, test])
def check(c):
    """Run all code checks."""
