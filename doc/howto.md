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