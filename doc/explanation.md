# Explanations

## Affiliations workflow diagrams

We have diagrams for our current and desired affiliations workflow in the
[diagrams directory](./diagrams).

## Environment variables

There's a `.env.template` file that is the source of truth for environment
variable keys. You're supposed to create a `.env` file file based on
`.env.template`. The keys in each environment variable file should stay the same
at all times. This is enforced programmatically using Invoke tasks. (See the
`tasks.py` file for more details on this.) The values of the keys can differ
between files, of course.
