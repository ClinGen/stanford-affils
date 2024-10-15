# 2. Summary of decisions thus far

Date: 2024-10-09

## Status

Accepted

## Context

This is a high-level summary of previous decisions that have been made on this
project. ADRs will be used for all new architectural decisions.

## Decision

Below is a list with the specific explanations on the architectural decisions
that have been made thus far in this project.

#### Use Django and Django Admin.

Previously, we were using Flask to implement a simple web application, and we
were building our own custom HTML templates. Then we then decided that Django's
admin panel had most of what we needed in terms of UI. It was felt that
utilizing Django's built-in admin site could easily support the projected user
base size of the Affiliations Microservice and it would increase the speed of
delivery on this project. It was also a benefit that it was another Python
framework and a tool being utilized on another project on the team to create
cross over skills.

Although it is not recommended to base your website solely on the built-in admin
site, since this is going to be a small internal tool to replace a spreadsheet
and JSON files, that will later be mostly handled by API request via the GPM we
felt that it would serve our purposes; we acknowledged that the recommendations
and limitations that would be brought on by building our service solely on top
of the built-in Django admin site.

#### Using PostgreSQL

We were interested in a relational database management system and PostgreSQL has
many features that are supported by Django. Postgres is also recommended as the
database back-end by the creators of Django.

#### Using Unfold Admin

After discussion of the base Django Admin UI not aligning with our vision of the
project, we discussed the making custom CSS vs finding a pre-built theme to
utilize. With the resources we had available, using a pre-built theme we can
tweak and customize seemed like a better use of time. After looking at several
options, we settled on Unfold Admin not only because of the styling, but because
it was well supported and the community seemed active surrounding it.

#### Using Custom JS

Our goal in this project is to not make it overly complex. It is meant to be a
simple internal tool and we want the design to reflect that. So creating a
custom and slightly more complex design choice was weighed heavily before
implementation. This choice was to make it easier for users to create new
Affiliations and automate as many choices as possible for them.

Why not just remove the fields from the Admin service instead of hiding with JS?
With how Django Admin needs to ingest the data to create an affiliation in the
database, these fields need to be a part of the Admin fields. However, since we
are automating the data in these fields, we need to hide them from the user.
This seemed like the most simple choice for this more complex decision and
request.

#### Using ASGI and Daphne

We decided to use ASGI in comparison to WSGI to deploy this application because
in later iterations of this app, we will be communicating with multiple APIs,
which ASGI handles better because of the async capabilities. From our
understanding, it is difficult to transition from WSGI to ASGI if it is needed
later in the application life-span; and is recommended to start out with ASGI if
you believe you might need it later.

We also decided to use Daphne as it was created by the same group that created
Django, so it seemed like an easy option to implement. There were no big
downsides to choosing other options, but this fact made it easier to decide
which option to move forward with.

## Consequences

Since we built directly on top of the Django admin site, we have limited
ourselves in some way to how easy/difficult it will be to make certain changes
and customizations based on user feedback. In addition, adding custom UI should
not be a difficult task in future iterations if it is needed. We weighed this
against the projected user pool for this application and the reality that many
of these manual user inputs will be done via API in later iterations.
