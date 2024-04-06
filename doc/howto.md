# How-to guides

## Run code checks

Code should be:

1. automatically formatted using [Black](https://github.com/psf/black),
2. linted using [Pylint](https://github.com/pylint-dev/pylint),
3. type-checked using [mypy](https://mypy-lang.org/), and
4. tested using [Pytest](https://github.com/pytest-dev/pytest/).

To run these checks:

```
inv check
```

## Organize imports and constants

At the top of any given module there will probably be imports and
constants. Our preferred way of organizing them is as follows:

```
# Built-in libraries:
# [Built-in libraries go here.]

# Third-party dependencies:
# [Third-party dependencies installed via Pipenv go here.]

# In-house code:
# [In-house code imports go here.]

# Constants:
FOO = "foo"
BAR = 123
```

Each of the sections should be sorted alphabetically.

## Write a TODO comment

TODO comments should include the name of the person who wrote the TODO
comment and a link to a GitHub issue describing the TODO in more depth.

## Write a commit message

When writing a commit, follow the example provided here:

```
Describe how to write a good commit

The first line of a commit message serves as a summary. When displayed
on the web, it's often styled as a heading, and in emails, it's
typically used as the subject. As such, you should capitalize it and
omit any trailing punctuation. Aim for about 50 characters, give or
take, otherwise it may be painfully truncated in some contexts. Write
it, along with the rest of your message, in the imperative tense: "Fix
bug" and not "Fixed bug" or "Fixes bug". Consistent wording makes it
easier to mentally process a list of commits.

Oftentimes a subject by itself is sufficient. When it's not, add a blank
line (this is important) followed by one or more paragraphs hard wrapped
to 72 characters. Git is strongly opinionated that the author is
responsible for line breaks; if you omit them, command line tooling will
show it as one extremely long unwrapped line. Fortunately, most text
editors are capable of automating this.

A commit should almost always be linked to a GitHub issue.

For:
https://github.com/org/repo/issues/123
```

## Set up Postgres locally

This how-to guide assumes you are using macOS. The steps will be
different for different operating systems.

- Install Postgres: `brew install postgresql@16`
- Start Postgres now and restart at login: `brew services start postgresql@16`
- Add Postgres to your PATH: `export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"`
    - If you are using Zsh (the default shell on macOS), I believe this
      can go in `.zshrc` in your home directory.
    - If you use a different shell, the file you put this in might be
      different, and the syntax might be different.
- Either reload your shell configuration or restart your terminal
  session so Postgres executables will be on your PATH.
- Run `which psql`. You should see: `/opt/homebrew/opt/postgresql@16/bin/psql`
- Enter the Postgres shell as the default user: `psql postgres`
- Create the affiliations database: `CREATE DATABASE affils;`
- Create a new user for the affiliations service:
```
CREATE USER affils WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE affils TO affils;
```
- Change the owner of the database:
```
ALTER DATABASE affils OWNER TO affils;
```
- Create and fill out a `.env.local` file in the root of the
  affiliations repository.
    - The values you should fill in should be in the `.env.template`
      file.
    - See [the doc on environment variables](./envars.md) for more info
      on environment variables.
    - The default Postgres port is 5432.
    - For local development, the host should be localhost.

## View info on AWS

The affils service is deployed to AWS's Elastic Beanstalk service. If
you use your Stanford credentials to log in to AWS, choose the
production profile, and set your region to Oregon (us-west-2), and then
you navigate to the Elastic Beanstalk console, you should see an Elastic
Beanstalk environment called `affils-env`. The `affils-env` environment
contains the `affils` application. If you click the `affils`
application, you should be able to view information about the affils
service.

## View logs on AWS

When running locally, logs are written to stdout. When running on AWS,
logs can be viewed in CloudWatch. To view the logs, navigate to the
CloudWatch web console, then in the side bar click the link to the log
groups page. Then look for the `web.stdout.log` log group. Then click
the appropriate log stream (probably the most recent one).

## Deploy to AWS

To deploy the files from your computer, enter the following:

```
inv deploy
```

This command should upload the affils files from your computer to AWS's
Elastic Beanstalk service.