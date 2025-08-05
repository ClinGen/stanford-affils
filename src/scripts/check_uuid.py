# pylint: disable=duplicate-code

"""
Script to be run to check data in DB vs in spreadsheet.

CSV needs to be saved in the `scripts` folder in directory before running.

You can then run this script by running: 
`python manage.py runscript add_uuid` in the command line from the directory.

Follow steps outlined in [tutorial.md](
doc/tutorial.md/#running-the-loadpy-script-to-import-data-into-the-database).
"""

import csv
from pathlib import Path

from django.db import transaction
from affiliations.models import Affiliation

CSV_FILE = Path(__file__).parent / "gpm-expert-panel_custom.csv"


@transaction.atomic
def run():
    """
    Iterate through a CSV, check if affiliation data matches what is in CSV
    """
    with open(CSV_FILE, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

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
                uuid_compare = affil.uuid == uuid_value
                full_name_compare = affil.full_name == long_name
                short_name_compare = affil.short_name == short_name
                if uuid_compare is False:
                    print(f"{affil.uuid} != {uuid_value}")
                if full_name_compare is False:
                    print(f"{affil.full_name} != {long_name}")
                if short_name_compare is False:
                    print(f"{affil.short_name} != {short_name}")
