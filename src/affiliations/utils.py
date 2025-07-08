"""Utility functions"""

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


def validate_and_set_expert_panel_id(cleaned_data: dict) -> None:
    """Assign expert_panel_id based on type and affiliation_id,
    then validate related CDWG requirements."""
    affil_id = cleaned_data.get("affiliation_id")
    _type = cleaned_data.get("type")
    cdwg = cleaned_data.get("clinical_domain_working_group")

    if affil_id is None:
        raise ValidationError("affiliation_id is required to create expert_panel_id.")

    ep_id = None

    if _type == "VCEP":
        ep_id = (affil_id - AFFIL_BASE) + VCEP_BASE
        if not VCEP_BASE <= ep_id < 60000:
            raise ValidationError("VCEP ID out of range. Contact administrator.")

    elif _type == "SC_VCEP":
        ep_id = (affil_id - AFFIL_BASE) + VCEP_BASE
        if not VCEP_BASE <= ep_id < 60000:
            raise ValidationError("SC-VCEP ID out of range. Contact administrator.")

        expected_cdwg = ClinicalDomainWorkingGroup.objects.get(name="Somatic Cancer")
        if cdwg != expected_cdwg:
            raise ValidationError(
                "If type is 'Somatic Cancer Variant Curation Expert Panel', "
                + "then CDWG must be 'Somatic Cancer'."
            )

    elif _type == "GCEP":
        ep_id = (affil_id - AFFIL_BASE) + GCEP_BASE
        if not GCEP_BASE <= ep_id < VCEP_BASE:
            raise ValidationError("GCEP ID out of range. Contact administrator.")
    else:
        expected_cdwg = ClinicalDomainWorkingGroup.objects.get(name="None")
        if cdwg != expected_cdwg:
            raise ValidationError(
                "If type is 'Independent Curation Group', then CDWG must be 'None'."
            )

    cleaned_data["expert_panel_id"] = ep_id
