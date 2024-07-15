"""Apps for the affiliations service."""

# Third-party dependencies:
from django.apps import AppConfig


class AffiliationsConfig(AppConfig):
    """Configure the affiliations application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "affiliations"
