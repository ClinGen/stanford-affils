<div align=center>
<h1>Affiliations Service</h1>

[Production Site](https://affils.clinicalgenome.org/) |
[Test Site](https://affils-test.clinicalgenome.org/)

[![continuous integration](https://github.com/clingen/stanford-affils/actions/workflows/check.yml/badge.svg)](https://github.com/ClinGen/stanford-affils/actions)
[![production uptime](https://img.shields.io/uptimerobot/status/m800645434-fff5912d3d952246a0a8d2e3)](https://stats.uptimerobot.com/fcfUfhnSRA)
</div>

The affiliations service is an internal ClinGen tool used to manage 
groups of curators for the gene curation interface (GCI) and the variant
curation interface (VCI).

The affiliations service is maintained by the Stanford contingent of
[ClinGen](https://clinicalgenome.org).

## Getting Started

- Install [Pipenv](https://pipenv.pypa.io/).
- Clone the repository.
- Install dependencies: `pipenv --sync dev`.
- [Set up Postgres for local development.](./doc/how-to.md#set-up-postgres-for-local-development)
- Create and populate a `.env` file in the root of the repository.
- Run the development server: `cd src && python manage.py runserver`.
  - As of 2025-09-16, you will need to modify your `settings.py` 
    module to run locally. Follow these steps:
    - Set `DEBUG` to `True`.
    - Add `127.0.0.1` to `ALLOWED_HOSTS`.
    - Comment out the `LOGGING` block.

## Documentation

- [Tutorials](./doc/tutorial.md)
- [How-To Guides](./doc/how-to.md)
- [Explanations](./doc/explanation.md)
- [Reference Guides](./doc/reference.md)

## Contributing

You are welcome to submit a
[bug report](https://github.com/clingen/stanford-affils/issues/new)
or a [pull request](https://github.com/ClinGen/stanford-affils/compare).

## License

The affiliation service's source code is subject to the MIT License. 
Read the text of the license [here](./LICENSE.md).
