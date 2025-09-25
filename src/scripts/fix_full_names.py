"""Adds 'GCEP' or 'VCEP' suffix to the full name of an affiliation.

On September 25th, Matt opened an issue about affiliation names missing their 'GCEP' or
'VCEP' suffix in the curation interface. I (Liam) believe this change crept in when we
imported UUIDs from the GPM, around August 14th. When we were importing UUIDs, we also
overwrote the full name and short name of the affiliation with the full name and short
name from the GPM. This was bad because the GPM didn't have the GCEP and VCEP suffixes
in the full names.
"""

from affiliations.models import Affiliation

GCEP = "GCEP"
VCEP = "VCEP"


def add_suffix(full_name: str, suffix: str) -> str:
    """Adds a suffix to the full name if necessary.

    Args:
        full_name: The full name of the affiliation.
        suffix: The suffix to add.

    Returns:
        The full name of the affiliation with the suffix added if it needed to be added
        or the original name otherwise.
    """
    if full_name[-4:] != suffix:
        return f"{full_name} {suffix}"
    return full_name


def run() -> None:
    """Iterates through affiliations adding the suffix if necessary."""
    affiliations = Affiliation.objects.all()
    for a in affiliations:
        if a.type == GCEP:
            a.full_name = add_suffix(a.full_name, GCEP)
            a.save()
        elif a.type == VCEP:
            a.full_name = add_suffix(a.full_name, VCEP)
            a.save()
