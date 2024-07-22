"""Models of the data in the affiliations service."""

# Third-party dependencies:
from django.db import models


class Affiliation(models.Model):
    """Define the shape of an affiliation."""

    affiliation_id: models.IntegerField = models.IntegerField()
    name: models.CharField = models.CharField()
    status: models.CharField = models.CharField()
    type: models.CharField = models.CharField()
    family: models.CharField = models.CharField()
    members: models.CharField = models.CharField()

    def __str__(self):
        """Provide a string representation of an affiliation."""
        return f"Affiliation {self.affiliation_id} {self.name}"


class SubmitterId(models.Model):
    affiliation = models.ForeignKey(Affiliation, null=True, on_delete=models.CASCADE)
    clinvar_submitter_id: models.CharField = models.CharField()


class Approver(models.Model):
    affiliation = models.ForeignKey(Affiliation, null=True, on_delete=models.CASCADE)
    approver: models.CharField = models.CharField()


class Coordinator(models.Model):
    """Define the shape of coordinator objects"""

    affiliation = models.ForeignKey(Affiliation, null=True, on_delete=models.CASCADE)
    coordinator_name: models.CharField = models.CharField(max_length=200)
    coordinator_email: models.EmailField = models.EmailField()

    def __str__(self):
        """Provide a string for header"""
        return self.coordinator_name
