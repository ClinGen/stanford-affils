# Tutorials

Description from
[Divio documentation](https://docs.divio.com/documentation-system/tutorials/):

Tutorials are lessons that take the reader through a series of steps to complete
a project of some kind. This page is learning-oriented, and specifically,
oriented towards learning how rather than learning what.

## Get started

- Install Python 3.10+.
- Install [Pipenv](https://pipenv.pypa.io/en/latest/index.html):
  `pip install --user pipenv`.
- Activate a virtual environment: `pipenv shell`.
- Install dependencies: `pipenv sync --dev`.
- Create a `.env` file based on `.env.template`.
- [Set up Postgres for local development](./howto.md#set-up-postgres-for-local-development).
- Run the development server: `cd src`, then `python manage.py migrate`.
- Run the development server: `cd src`, then `python manage.py runserver`.
- Install [yamlfmt](https://github.com/google/yamlfmt): `brew install yamlfmt`.

## Running the load.py script to import CSV data into the database

- Make sure all dependencies are synced: `pipenv sync --dev`.
- Save CSV into `scripts` folder in directory.
- Run `python manage.py runscript load`.

## Running database backup

- Make sure all dependencies are synced: `pipenv sync --dev`.
- Make sure AWS S3 bucket is configured and env variables are in .env file.
- Run `python manage.py dbbackup`.

## Restoring database from backup

- Make sure all dependencies are synced: `pipenv sync --dev`.
- Make sure AWS S3 bucket is configured and env variables are in .env file.
- Run `python manage.py dbrestore`.
- To see previous backups you can display the backup list with
  `python manage.py listbackups` and restore a specific backup with
  `python manage.py dbrestore -i {file-name}`
