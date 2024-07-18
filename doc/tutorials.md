# Tutorials

Description from
[Divio documentation](https://docs.divio.com/documentation-system/tutorials/):

Tutorials are lessons that take the reader through a series of steps
to complete a project of some kind.
This page is learning-oriented, and specifically, oriented towards learning
how rather than learning what.

## Setting Up Your Environment

1. Install Python 3.12+.
2. Install [Pipenv](https://pipenv.pypa.io/en/latest/index.html):
   `pip install --user pipenv`.
3. Activate a virtual environment: `pipenv shell`.
4. Install dependencies: `pipenv sync --dev`.
5. Create a `.env` file based on `.env.template`.
   - See our explanation guide on [environment variables here](./how-to.md#environment-variables)
6. Seed the database: `inv dbseed`.
7. Run the development server: `inv dev`.
8. Install optional [yamlfmt](https://github.com/google/yamlfmt): `brew install yamlfmt`
