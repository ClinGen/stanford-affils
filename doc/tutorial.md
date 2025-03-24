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

## Running the load.py script to import data into the database

- Make sure all dependencies are synced: `pipenv sync --dev`.
- Save file into `scripts` folder in directory.
- Run `python manage.py runscript {script_name}`.

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

## Adding logs

- First add `import logging` to the top of the file.
- Then add the below two lines of code (changing log level, string, and
  variables as needed): `logger = logging.getLogger("watchtower")`
  `logger.info(f"Affiliation Created:\\n\\n {Affiliation.full_name} (PK: {Affiliation.pk})")`
- The desired log line will appear in the selected logging handler.

## API Key Information

- We are utilizing
  [Django REST Framework API Key](https://florimondmanca.github.io/djangorestframework-api-key/)
  package to support the use of API keys.

### API KEY

- If you are in need of an API Key, please reach out to one of the website
  administrators or your admin user to obtain an API Key.
- Upon creating an API key from the admin, the full API key is shown only once
  in a success message banner. After creation, only the prefix of the API key is
  shown in the admin site, mostly for identification purposes. If you lose the
  full API key, you'll need to regenerate a new one.

### Authorization

Clients must pass their API key via an HTTP header. It
must be formatted as follows: `X-Api-Key: <API_KEY>` where
\<API_KEY> refers to the full generated API key.

### Endpoints
`affiliations_list/`

`affiliation_detail/?affil_id={affiliation_id}`

### URLS
TEST:
`https://affils-test.clinicalgenome.org/api/`

PROD:
`https://affils.clinicalgenome.org/api/`

Examples:
`https://affils-test.clinicalgenome.org/api/affiliations_list/` will give you a 
JSON response of all affiliations.

If you set the environment variable `AFFILIATIONS_API_KEY` with your API key, you
can get data from the command-line with any of the following tools:

```bash
# HTTPie
http https://affils-test.clinicalgenome.org/api/affiliations_list/ "X-Api-Key:$AFFILIATIONS_API_KEY"
# curl
curl -H "X-Api-Key:$AFFILIATIONS_API_KEY" https://affils-test.clinicalgenome.org/api/affiliations_list/
# wget
wget --header "X-Api-Key: $AFFILIATIONS_API_KEY" https://affils-test.clinicalgenome.org/api/affiliations_list/ -O-
```

