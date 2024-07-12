# Documentation

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

## Write code that can be submitted to the main branch

- Must pass the `check` script.
- New code must have automated tests.
- New code must have docstrings.
- If adding a new tool or something that other developers need to understand,
  there must be a tutorial for it.
- If a manual process is being added, there must be a how-to guide for it.
- If changing something significant (e.g. architecture) there should be a
  written explanation.
- If doing something complex or weird, there should be an explanation for it.

## Organize imports and constants

At the top of any given module there will probably be imports and constants. Our
preferred way of organizing them is as follows:

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

## Environment variables

There's a `.env.template` file that is the source of truth for environment
variable keys. You're supposed to create a `.env` file file based on
`.env.template`. The keys in each environment variable file should stay the same
at all times. This is enforced programmatically using Invoke tasks. (See the
`tasks.py` file for more details on this.) The values of the keys can differ
between files, of course.
