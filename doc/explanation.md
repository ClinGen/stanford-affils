# Explanations

Description from
[Divio documentation](https://docs.divio.com/documentation-system/explanation/):

Explanations, or discussions, should clarify and illuminate a particular topic.
They should broaden the documentation’s coverage of a topic. This page is
understanding-oriented.

## Affiliations Workflow Diagrams

We have diagrams for our current and desired affiliations workflow in the
[diagrams directory](./diagrams).

## Styling

We use
[django-unfold](https://github.com/unfoldadmin/django-unfold?tab=readme-ov-file)
to style the Django admin panel.

## Architecture Decision Records (ADRs)

We utilize ADRs documentation to make it easier for future contributors to
understand our reasons for implementation choices and rationale.

Please utilize is the template in
[Documenting architecture decisions - Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions),
and also
[documented in github here](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-michael-nygard/index.md).

For more information on ADRs, please visit some of the below resources:

- https://www.redhat.com/architect/architecture-decision-records
- https://adr.github.io/

We are utilizing [adr-tools-python](https://pypi.org/project/adr-tools-python/),
additional information can be found in their documentation.

- Can create a new ADR by using `adr-new {name of adr}`.
- Can utilize `adr-list` to see a list of all ADRs in the terminal.
