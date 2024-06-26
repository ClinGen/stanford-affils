"""Script for running any/all command line tasks for this project.

All command line tasks should be defined in this file. The only
exception to this is managing dependencies via Pipenv.
"""

# Invoke always requires a context parameter, even if it ends up going
# unused. As of this writing, there are a handful of tasks that don't
# use their context parameters.
# pylint: disable=unused-argument

# Built-in libraries:
import sys

# Third-party dependencies:
from dotenv import dotenv_values
from invoke import task

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


@task
def types(c):
    """Check types."""
    c.run("mypy .")


@task
def test(c):
    """Run the test suite."""
    c.run("coverage run -m pytest && coverage report")


@task
def sqlschema(c):
    """Generate a schema SQL script.

    This script will create the necessary table(s) and columns.

    This task assumes you are in the root directory of the repo.
    """
    c.run(
        f"sqlite3 {ACTUAL_CONF.get("AFFILS_DB_NAME", "affils.db")} .schema > ./src/sql/schema.sql"
    )


@task
def sqldump(c):
    """Generate a dump SQL script.

    This script can be used to seed the DB with some values.

    This task assumes you are in the root directory of the repo.
    """
    c.run(
        f"sqlite3 {ACTUAL_CONF.get("AFFILS_DB_NAME", "affils.db")} .dump > ./src/sql/dump.sql"
    )


@task
def sqlfmt(c):
    """Format the SQL scripts."""
    c.run("sqlfluff format --dialect sqlite")


@task
def sqlfix(c):
    """Attempt to auto-fix SQL scripts."""
    c.run("sqlfluff fix --dialect sqlite")


@task
def sqllint(c):
    """Lint the SQL scripts."""
    c.run("sqlfluff lint --dialect sqlite")


@task
def envsame(c):
    """Ensure environment variable keys match."""
    if TEMPLATE_CONF.keys() != ACTUAL_CONF.keys():
        print(".env keys do not match. Check your .env files.")
        sys.exit(1)


@task(pre=[fmt, lint, types, test, sqlfmt, sqlfix, sqllint, envsame])
def check(c):
    """Run all code checks."""
    # Also lint this file.
    c.run("pylint tasks.py")


@task
def dbmake(c):
    """Create the affiliations database if it doesn't exist.

    This task assumes you are in the root directory of the repo.
    """
    # Here we don't use the environment variable for the database name
    # because we want to avoid complexity in GitHub Actions. (I don't
    # want to manually add environment variables to GitHub Actions.)
    c.run("sqlite3 affils.db < ./src/sql/schema.sql")


@task
def dbseed(c):
    """Seed the affiliations database with values.

    This task assumes you are in the root directory of the repo.
    """
    # Here we don't use the environment variable for the database name
    # because we want to avoid complexity in GitHub Actions. (I don't
    # want to manually add environment variables to GitHub Actions.)
    c.run("sqlite3 affils.db < ./src/sql/dump.sql")


@task
def dev(c):
    """Run the development server.

    Assumes you've activated the virtual environment. Also assumes
    you're in the root directory.
    """
    # c.run(f"source {ENV_ACTUAL} && cd src && flask run -p 8080")

    c.run(f"source {ENV_ACTUAL} && echo $AFFILS_DB_FILE && cd src && flask run -p 8080")