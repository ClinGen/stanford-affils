"""Models of the data in the affiliations service."""

# Third-party dependencies:
from django.db import models


class Affiliation(models.Model):
    """Define the shape of an affiliation."""

    type: models.CharField = models.CharField()
    """
    10000 ID. All affiliations will have this ID, however, some affiliations
    will share this ID. Affiliations that share this ID will have different
    curation_panel_ids.
    """
    affiliation_id: models.IntegerField = models.IntegerField(
        help_text="10000 number ID"
    )
    """
    4000 or 5000 ID. This ID can be null as independent groups will not have
    either of these IDs.
    """
    curation_panel_id: models.IntegerField = models.IntegerField(
        blank=True,
        null=True,
        help_text="GCEP or VCEP ID. If Independent Curation Group, leave this field blank.",
    )
    full_name: models.CharField = models.CharField()
    abbreviated_name: models.CharField = models.CharField(blank=True, null=True)
    status: models.CharField = models.CharField()
    clinical_domain_working_group: models.CharField = models.CharField()
    members: models.CharField = models.CharField()

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


class Submitter(models.Model):
    """Define the shape of an submitter."""

    affiliation = models.ForeignKey(
        Affiliation, related_name="clinvar_submitter_ids", on_delete=models.CASCADE
    )  # type: object
    clinvar_submitter_id: models.CharField = models.CharField()
