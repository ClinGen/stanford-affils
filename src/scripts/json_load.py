"""
Script to be run to insert existing data from 
the affiliations JSON file to the database.

JSON file needs to be saved in the `scripts` folder in directory before running.

You can then run this script by running: 
`python manage.py runscript json_load` in the command line from the directory.

Follow steps outlined in [tutorial.md](
doc/tutorial.md/#running-the-loadpy-script-to-import-data-into-the-database).
"""

from pathlib import Path
import json
from affiliations.models import Affiliation, Approver

FILEPATH = Path(__file__).parent / "affiliations.json"


def run():
    """Iterate through JSON file and update Affiliation with Approver
    objects in the DB."""
    count = 0
    with open(FILEPATH, encoding="utf-8") as json_file:

        data = json.load(json_file)
        for item in data:
            if "approver" in item:
                affiliation_id = item["affiliation_id"]
                approver = item["approver"]
                if "subgroups" in item:
                    if "vcep" in item["subgroups"]:
                        vcep_id = item["subgroups"]["vcep"]["id"]
                        affil_obj = Affiliation.objects.get(
                            affiliation_id=affiliation_id, expert_panel_id=vcep_id
                        )
                        create_approver_model(approver, affil_obj, count)

                    if "gcep" in item["subgroups"]:
                        gcep_id = item["subgroups"]["gcep"]["id"]
                        affil_obj = Affiliation.objects.get(
                            affiliation_id=affiliation_id, expert_panel_id=gcep_id
                        )
                        create_approver_model(approver, affil_obj, count)
                else:
                    affil_obj = Affiliation.objects.get(affiliation_id=affiliation_id)
                    create_approver_model(approver, affil_obj, count)
        print(count, "changed")


def create_approver_model(approver, affil_obj, count):
    """Check if approver exists, if not create approver foreign key model."""
    for approver_name in approver:
        if not (
            Approver.objects.filter(
                affiliation=affil_obj,
                approver_name=approver_name,
            ).exists()
        ):
            count += 1
            Approver.objects.create(
                affiliation=affil_obj,
                approver_name=approver_name,
            )
