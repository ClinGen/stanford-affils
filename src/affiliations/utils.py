"""Utility functions"""

from uuid import UUID
from django.db import transaction
from django.core.exceptions import ValidationError
from affiliations.models import Affiliation, ClinicalDomainWorkingGroup


VCEP_BASE = 50000
GCEP_BASE = 40000
AFFIL_BASE = 10000


def generate_next_affiliation_id(cleaned_data: dict) -> None:
    """Generate the next sequential affiliation_id as an integer."""
    with transaction.atomic():
        existing_ids = (
            Affiliation.objects.select_for_update()
            .values_list("affiliation_id", flat=True)
            .order_by("affiliation_id")
        )

        if existing_ids:
            last_id = max(existing_ids)
            next_id = last_id + 1
        else:
            next_id = AFFIL_BASE

        if next_id < AFFIL_BASE or next_id >= 20000:
            raise ValidationError("Affiliation ID out of range. Contact administrator.")

        cleaned_data["affiliation_id"] = next_id


def set_expert_panel_id(cleaned_data: dict) -> None:
    """Assign expert_panel_id based on type and affiliation_id."""
    affil_id = cleaned_data.get("affiliation_id")
    type_ = cleaned_data.get("type")

    if affil_id is None:
        raise ValidationError("affiliation_id is required to create expert_panel_id.")

    ep_id = None

    if type_ == "VCEP":
        ep_id = (affil_id - AFFIL_BASE) + VCEP_BASE
        if not VCEP_BASE <= ep_id < 60000:
            raise ValidationError("VCEP ID out of range. Contact administrator.")

    elif type_ == "SC_VCEP":
        ep_id = (affil_id - AFFIL_BASE) + VCEP_BASE
        if not VCEP_BASE <= ep_id < 60000:
            raise ValidationError("SC-VCEP ID out of range. Contact administrator.")

    elif type_ == "GCEP":
        ep_id = (affil_id - AFFIL_BASE) + GCEP_BASE
        if not GCEP_BASE <= ep_id < VCEP_BASE:
            raise ValidationError("GCEP ID out of range. Contact administrator.")

    cleaned_data["expert_panel_id"] = ep_id


def validate_unique_cdwg_name(name: str, instance_id=None) -> None:
    """
    Raise ValidationError if another CDWG with the same name exists.
    Case-insensitive check. Allows the current instance to retain its name.
    """
    qs = ClinicalDomainWorkingGroup.objects.all()
    if instance_id:
        qs = qs.exclude(id=instance_id)
    if qs.filter(name__iexact=name).exists():
        raise ValidationError(
            "A Clinical Domain Working Group with this name already exists."
        )


def validate_cdwg_matches_type(cleaned_data: dict, instance=None) -> None:
    """Ensure the provided CDWG is valid for the given immutable type."""
    type_ = cleaned_data.get("type")
    cdwg = cleaned_data.get("clinical_domain_working_group")

    if not type_ and instance:
        type_ = getattr(instance, "type", None)
    if not cdwg:
        return

    if type_ == "SC_VCEP":
        expected = ClinicalDomainWorkingGroup.objects.get(name="Somatic Cancer")
        if cdwg != expected:
            raise ValidationError(
                "If type is 'Somatic Cancer Variant Curation Expert Panel', "
                + "then CDWG must be 'Somatic Cancer'."
            )

    elif (
        type_ == "INDEPENDENT_CURATION"
    ):  # If your type for independent groups is 'ICG'
        expected = ClinicalDomainWorkingGroup.objects.get(name="None")
        if cdwg != expected:
            raise ValidationError(
                "If type is 'Independent Curation Group', then CDWG must be 'None'."
            )
def check_duplicate_affiliation_uuid(uuid_val: UUID, instance=None) -> bool:
    """Check if an affiliation with the given UUID already exists."""
    if uuid_val is None:
        return False
    uuid_value = Affiliation.objects.filter(uuid=uuid_val)
    if instance:
        uuid_value = uuid_value.exclude(pk=instance.pk)
    return uuid_value.exists()


def validate_type_and_uuid(cleaned_data: dict) -> None:
    """Validate that Independent Groups do not have UUIDs."""
    uuid_val = cleaned_data.get("uuid")
    type_val = cleaned_data.get("type")

    if type_val == "INDEPENDENT_CURATION":
        if uuid_val:
            raise ValidationError("UUID must be empty for 'INDEPENDENT_CURATION' type.")
