"""Models of the data in the affiliations service."""

# Third-party dependencies:
from django.db import models


class Affiliation(models.Model):
    """Define the shape of an affiliation."""

    affiliation_id: models.IntegerField = models.IntegerField()
    full_name: models.CharField = models.CharField()
    abbreviated_name: models.CharField = models.CharField(blank=True, null=True)
    status: models.CharField = models.CharField()
    type: models.CharField = models.CharField()
    clinical_domain_working_group: models.CharField = models.CharField()
    members: models.CharField = models.CharField()
    clinvar_submitter_ids: models.CharField = models.CharField()

    def __str__(self):
        """Provide a string representation of an affiliation."""
        return f"Affiliation {self.affiliation_id} {self.full_name}"


class Coordinator(models.Model):
    """Define the shape of an coordinator."""

    affiliation = models.ForeignKey(
        Affiliation, related_name="coordinators", on_delete=models.CASCADE
    )  # type: object
    coordinator_name: models.CharField = models.CharField()
    coordinator_email: models.EmailField = models.EmailField()


class Approver(models.Model):
    """Define the shape of an approver."""

    affiliation = models.ForeignKey(
        Affiliation, related_name="approvers", on_delete=models.CASCADE
    )  # type: object
    approver_name: models.CharField = models.CharField()
