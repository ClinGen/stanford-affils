"""Models of the data in the affiliations service."""

# Third-party dependencies:
from django.db import models
from django.utils.translation import gettext_lazy as _


class AffiliationStatus(models.TextChoices):  # pylint: disable=too-many-ancestors
    """Creating choices for status."""

    APPLYING = "APPLYING", _("Applying")
    ACTIVE = "ACTIVE", _("Active")
    INACTIVE = "INACTIVE", _("Inactive")
    RETIRED = "RETIRED", _("Retired")
    ARCHIVED = "ARCHIVED", _("Archived")


class AffiliationType(models.TextChoices):  # pylint: disable=too-many-ancestors
    """Creating choices for type."""

    VCEP = "VCEP", _("Variant Curation Expert Panel")
    GCEP = "GCEP", _("Gene Curation Expert Panel")
    INDEPENDENT_CURATION = "INDEPENDENT_CURATION", _("Independent Curation Group")
    SC_VCEP = "SC_VCEP", _("Somatic Cancer Variant Curation Expert Panel")


class AffiliationCDWG(models.TextChoices):  # pylint: disable=too-many-ancestors
    """Creating choices for clinical_domain_working_group."""

    NONE = "NONE", _("None")
    CARDIOVASCULAR = "CARDIOVASCULAR", _("Cardiovascular")
    HEARING_LOSS = "HEARING_LOSS", _("Hearing Loss")
    HEMOSTASIS_THROMBOSIS = "HEMOSTASIS_THROMBOSIS", _("Hemostasis/Thrombosis")
    HEREDITARY_CANCER = "HEREDITARY_CANCER", _("Hereditary Cancer")
    IMMUNOLOGY = "IMMUNOLOGY", _("Immunology")
    INBORN_ERR_METABOLISM = "INBORN_ERR_METABOLISM", _("Inborn Errors of Metabolism")
    KIDNEY_DISEASE = "KIDNEY_DISEASE", _("Kidney Disease")
    NEURODEVELOPMENTAL_DISORDER = "NEURODEVELOPMENTAL_DISORDER", _(
        "Neurodevelopmental Disorders"
    )
    NEUROLOGICAL_DISORDERS = "NEUROLOGICAL_DISORDERS", _("Neurological Disorders")
    OCULAR = "OCULAR", _("Ocular")
    OTHER = "OTHER", _("Other")
    PULMONARY = "PULMONARY", _("Pulmonary")
    RASOPATHY = "RASOPATHY", _("RASopathy")
    RHEUMA_AUTO_DISEASE = "RHEUMA_AUTO_DISEASE", _("Rheumatologic Autoimmune Disease")
    SKELETAL_DISORDERS = "SKELETAL_DISORDERS", _("Skeletal Disorders")
    SOMATIC_CANCER = "SOMATIC_CANCER", _("Somatic Cancer")


class Affiliation(models.Model):
    """Define the shape of an affiliation."""

    type: models.CharField = models.CharField(
        verbose_name="Type",
        choices=AffiliationType.choices,
    )
    """
    10000 ID. All affiliations will have this ID, however, some affiliations
    will share this ID. Affiliations that share this ID will have different
    expert_panel_ids.
    """
    affiliation_id: models.IntegerField = models.IntegerField(
        blank=True,
        verbose_name="Affiliation ID",
    )
    """
    40000 or 50000 ID. This ID can be null as independent groups will not have
    either of these IDs.
    """
    expert_panel_id: models.IntegerField = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Expert Panel ID",
    )
    full_name: models.CharField = models.CharField(verbose_name="Full Name")
    short_name: models.CharField = models.CharField(
        blank=True, null=True, verbose_name="Short Name"
    )
    status: models.CharField = models.CharField(
        verbose_name="Status",
        choices=AffiliationStatus.choices,
    )
    clinical_domain_working_group: models.CharField = models.CharField(
        verbose_name="CDWG",
        choices=AffiliationCDWG.choices,
    )
    members: models.CharField = models.CharField()
    is_deleted: models.BooleanField = models.BooleanField(default=False)

    def __str__(self):
        """Provide a string representation of an affiliation."""
        return f"Affiliation {self.affiliation_id} {self.full_name}"

    def delete(self, *args, **kwargs):
        """Override delete method to "soft-delete" affiliations."""
        self.is_deleted = True
        self.save(*args, **kwargs)


class Coordinator(models.Model):
    """Define the shape of an coordinator."""

    affiliation = models.ForeignKey(
        Affiliation, related_name="coordinators", on_delete=models.CASCADE
    )  # type: object
    coordinator_name: models.CharField = models.CharField(
        verbose_name="Coordinator Name"
    )
    coordinator_email: models.EmailField = models.EmailField(
        verbose_name="Coordinator Email"
    )


class Approver(models.Model):
    """Define the shape of an approver."""

    affiliation = models.ForeignKey(
        Affiliation, related_name="approvers", on_delete=models.CASCADE
    )  # type: object
    approver_name: models.CharField = models.CharField(verbose_name="Approver Name")


class Submitter(models.Model):
    """Define the shape of an submitter."""

    affiliation = models.ForeignKey(
        Affiliation, related_name="clinvar_submitter_ids", on_delete=models.CASCADE
    )  # type: object
    clinvar_submitter_id: models.CharField = models.CharField(
        verbose_name="ClinVar Submitter ID"
    )
