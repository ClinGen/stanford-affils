# Provides a simple way to run commands for this project.
#
# This file also documents command line "recipes" for this project. In order to use it,
# you must install the `just` program: https://github.com/casey/just.
#
# To list the available recipes and what they do, invoke `just -l` at the command line.
# (The dashes after the comment describing the recipe are there to help the formatting
# of the output of the `just -l` command.)
#
# NOTE: For the sake of simplicity, we assume the user of this justfile is invoking the
# recipes from the root of the repository. We also assume that the project's virtual
# environment has been activated.

# Load the .env file before we run commands.
set dotenv-load := true

#=====================================================================
# Pre-Commit Recipe
#=====================================================================

# Run all checks and tests. ------------------------------------------
pre-commit: misc-check-env-var-keys django-check py-all test-all
alias pre := pre-commit

#=====================================================================
# Continuous Integration Recipe
#=====================================================================

# Run all checks and tests that are run in CI. -----------------------
continuous-integration: py-format-check py-lint py-type-check test-all
alias ci := continuous-integration

#=====================================================================
# Python Recipes
#=====================================================================

# Run all Python code quality checks. --------------------------------
[group('python')]
py-all: py-format-check py-lint py-type-check
alias pyal := py-all

# Format the Python code. --------------------------------------------
[group('python')]
py-format:
    black src
alias pyfm := py-format

# Check the Python code for formatting issues. -----------------------
[group('python')]
py-format-check:
    black src --check
alias pyfc := py-format-check

# Check the Python code for lint errors. -----------------------------
[group('python')]
py-lint:
    pylint src
alias pylt := py-lint

# Check Python type hints. -------------------------------------------
[group('python')]
py-type-check:
    cd src && mypy .
alias pytc := py-type-check

#=====================================================================
# Test Recipes
#=====================================================================

# Run all tests. -----------------------------------------------------
[group('test')]
test-all:
    cd src && python manage.py test
alias tal := test-all

#=====================================================================
# Django Recipes
#=====================================================================

# Inspect the project for common problems. ---------------------------
[group('django')]
django-check:
    cd src && python manage.py check
alias djch := django-check

# Collect static files. ----------------------------------------------
[group('django')]
django-collectstatic:
    rm -rf src/staticfiles/
    cd src && python manage.py collectstatic
alias djcs := django-collectstatic

# Make migrations. ---------------------------------------------------
[group('django')]
django-makemigrations:
    cd src && python manage.py makemigrations
alias djmm := django-makemigrations

# Apply migrations. --------------------------------------------------
[group('django')]
django-migrate:
    cd src && python manage.py migrate
alias djmi := django-migrate

# Run the development server. ----------------------------------------
[group('django')]
django-runserver:
    cd src && python manage.py runserver
alias djru := django-runserver

# Enter the shell. ---------------------------------------------------
[group('django')]
django-shell:
    cd src && python manage.py shell
alias djsh := django-shell

#=====================================================================
# Miscellaneous Recipes
#=====================================================================

# Makes sure keys in .env.template match those in .env. --------------
[group('miscellaneous')]
misc-check-env-var-keys:
    cd src/scripts && python check_env_var_keys.py
alias miek := misc-check-env-var-keys
