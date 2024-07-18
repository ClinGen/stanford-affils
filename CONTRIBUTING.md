# Contributing Guidelines

Contributing and pull requests are welcome. If you would like to contribute,
please open an issue first to discuss that changes that you would like made.
Then follow the below documentation expectations.

## Best Practices

See our Gecko Group developer best practices spreadsheet
[here](https://docs.google.com/spreadsheets/d/1MLeEQE-v3eEnEtKNG4oJ8q6a8pal9q462TTgVcodcg4/edit?pli=1#gid=0).
We are also working toward conforming to OpenSSF Best Practices.
See [this page](https://www.bestpractices.dev/en/projects/8941) for more info.

## Documentation Guidelines

- Our [how-to guides](./doc/how-to.md). How to do specific tasks
  and documentation expectations.

## Opening an Issue

Before creating a new issue, please check to see if that issue has already
been raised.

### Bugs / Feature Requests

Please open an issue using the appropriate template detailing the issue you are
encountering or the improvement/suggestion that you have for the Affiliation
Service.

Please include any screenshots, screen recordings, and any examples with
detailed descriptions so our developers can investigate further.

## Submitting Pull Requests

- Please follow the [PR template](./doc/pull_request_template.md) when
  creating your PR.
- Smaller is better! A PR should preferably contain isolated changes
  pertaining to a single bug fix or feature request.
- Please follow the below coding style and conventions:

### Write a TODO comment

TODO comments should include the name of the person who wrote the TODO comment
and a link to a GitHub issue describing the TODO in more depth.

### Styling your Code

Defer to the formatter (Black) and the linter (pylint). If neither of them
have an opinion, refer to [Google's Python style guide](https://google.github.io/styleguide/pyguide.html).

### Write a Commit Message

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

### Name a Git Branch

Here is the format we like to follow for branch names:

```
[initials]-[issue number]-[optional description]
```

For example, if your name is Ada Lovelace and the issue you're working on is
#123 your branch name would be:

```
al-123
```

If you wanted to add an optional (short) description at the end, you could name
it:

```
al-123-fix-foobar
```
