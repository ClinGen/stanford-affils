# affils

affils is ClinGen's affiliations service.

## Getting started

The affils project uses [Pipenv](https://pipenv.pypa.io/en/latest/index.html)
to manage its dependencies. (Do not use the `requirements.txt` file.
The `requirements.txt` file is generated and used in GitHub Actions.)
For all other command line tasks, the affils project uses [Invoke](https://docs.pyinvoke.org/en/stable/index.html).

1. Install Python 3.12+.
2. Install [Pipenv](https://pipenv.pypa.io/en/latest/index.html): `pip install --user pipenv`.
3. Activate a virtual environment: `pipenv shell`.
4. Install dependencies: `pipenv sync --dev`.
5. Run the development server: `invoke dev` or `inv dev`.
6. Read the `tasks.py` module for other command line tasks.
7. Read the [standards document](./doc/standards.md).

## Affiliations workflow

We have diagrams for our current and desired affiliations workflow in
the [diagrams directory](./doc/diagrams).

## Environment variables

We use environment variables files (commonly referred to as `.env`
files) to configure the affiliations service. For more info on how we
use `.env` files, see the [doc on environment variables](./doc/envars.md).

## Deployment

Read the [doc](./doc/deploy.md) on deploying to production.
