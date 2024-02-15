# GitHub Actions workflows

This directory houses GitHub Actions workflows.

## Generating `requirements.txt`

GitHub Actions workflow runners don't play nicely with Pipenv, so we
generate a `requirements.txt` file by running `inv reqs`. We then use
this generated `requirements.txt` in GitHub Actions to install our
dependencies. The `inv reqs` command should be run whenever we update
our dependencies, which is annoying but slightly less annoying than
trying to get GitHub actions to work properly with Pipenv.

## Formatting YAML

To keep YAML files readable, run [yamlfmt](https://github.com/google/yamlfmt)
on them.