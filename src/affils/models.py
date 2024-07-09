"""Models of the data in the affiliations service."""

# Third-party dependencies:
from django.db import models


class Affiliation(models.Model):
    """Define the shape of an affiliation."""

    affiliation_id = models.IntegerField()
    name = models.CharField()
    coordinator = models.CharField()
    status = models.CharField()
    type = models.CharField()
    family = models.CharField()
    members = models.CharField()
    approvers = models.CharField()
    clinvar_submitter_ids = models.CharField()

    def __str__(self):
        """Provide a string representation of an affiliation."""
        return f"Affiliation {self.affiliation_id} {self.name}"
