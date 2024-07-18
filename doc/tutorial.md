# Tutorials

## Get started

- Install Python 3.12+.
- Install [Pipenv](https://pipenv.pypa.io/en/latest/index.html):
  `pip install --user pipenv`.
- Activate a virtual environment: `pipenv shell`.
- Install dependencies: `pipenv sync --dev`.
- Create a `.env` file based on `.env.template`.
- [Set up Postgres for local development](./howto.md#set-up-postgres-for-local-development).
- Run the development server: `cd src`, then `python manage.py migrate`.
- Run the development server: `cd src`, then `python manage.py runserver`.
- Install [yamlfmt](https://github.com/google/yamlfmt): `brew install yamlfmt`.
