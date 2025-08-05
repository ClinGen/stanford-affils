# pylint: disable=duplicate-code

"""
Script to be run to insert existing UUID data from
a spreadsheet to the database.

CSV needs to be saved in the `scripts` folder in directory before running.

You can then run this script by running:
`python manage.py runscript add_uuid` in the command line from the directory.

Follow steps outlined in [tutorial.md](
doc/tutorial.md/#running-the-loadpy-script-to-import-data-into-the-database).
"""

import csv
import uuid
from pathlib import Path

from django.db import transaction
from affiliations.models import Affiliation

CSV_FILE = Path(__file__).parent / "gpm-expert-panel_custom.csv"


@transaction.atomic
def run():
    """
    Iterate through a CSV, check if the ep_id and type match CSV,
    then add UUID to affiliation.
    """
    with open(CSV_FILE, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        updated = 0
        missing = []

        for row in reader:
            uuid_value = row["UUID"].strip()
            long_name = row["Long Name"].strip()
            short_name = row["Short Name"].strip()
            expert_panel_id = row["Affiliation ID"].strip()
            type_value = row["EP Type"].strip()

            affil = Affiliation.objects.filter(
                expert_panel_id=expert_panel_id, type=type_value
            ).first()
            if affil:
                try:
                    affil.uuid = uuid.UUID(uuid_value)
                    affil.full_name = long_name
                    affil.short_name = short_name
                    affil.save()
                    updated += 1
                except ValueError:
                    print(
                        f"Invalid UUID format for ID {expert_panel_id}, "
                        f"Type {type_value}: {uuid_value}"
                    )
            else:
                missing.append((expert_panel_id, type_value))

        print(f"{updated} affiliations updated with UUIDs.")
        if missing:
            print(f"{len(missing)} rows skipped (no match found):")
            for expert_panel_id, type_value in missing:
                print(f" - ID: {expert_panel_id}, Type: {type_value}")
