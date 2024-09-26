"""
Script to be run to insert existing data from 
the affiliations spreadsheet to the database.

CSV needs to be saved in the `scripts` folder in directory before running.

You can then run this script by running: 
`python manage.py runscript load` in the command line from the directory.

Follow steps outlined in [tutorial.md](
doc/tutorial.md/#running-the-loadpy-script-to-import-csv-data-into-the-database).
"""

import csv
from affiliations.models import Affiliation, Submitter, Coordinator


def run():  # pylint: disable-msg=too-many-locals
    """Iterate through CSV and create Affiliation, Submitter ID, and Coordinator
    objects in the DB."""

    with open(
        "/Users/gabriellasanchez/Desktop/repos/stanford-affils/src/scripts/test_affils.csv",
        encoding="utf-8",
    ) as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            external_full_name = row["Affiliation Full Name"].strip()
            affil_id = row["AffiliationID"].strip()
            coordinator_name = row["Coordinator(s)"].strip()
            coordinator_email = row["Email"].strip()
            clinvar_submitter_id = row["Submitter ID"]
            vcep_ep_id = row["VCEP Affiliation ID"].strip()
            vcep_full_name = row["VCEP Affiliation Name"].strip()
            gcep_ep_id = row["GCEP Affiliation ID"].strip()
            gcep_full_name = row["GCEP Affiliation Name"].strip()
            status = row["Status"].strip()
            cdwg = row["CDWG"].strip()

            coordinator_names = coordinator_name.split(",")
            coordinator_emails = coordinator_email.split(",")

            type_list = []
            if gcep_ep_id:
                type_list.append(("GCEP", gcep_ep_id, gcep_full_name))
            if vcep_ep_id:
                if "SC-VCEP" in vcep_full_name:
                    type_list.append(("SC_VCEP", vcep_ep_id, vcep_full_name))
                else:
                    type_list.append(("VCEP", vcep_ep_id, vcep_full_name))
            if not gcep_ep_id and not vcep_ep_id:
                type_list.append(("INDEPENDENT_CURATION", None, external_full_name))

            for type_name, ep_id, name in type_list:
                affil = Affiliation.objects.create(
                    affiliation_id=affil_id,
                    expert_panel_id=ep_id,
                    type=type_name,
                    full_name=name,
                    status=status,
                    clinical_domain_working_group=cdwg,
                )
                if clinvar_submitter_id != "":
                    Submitter.objects.create(
                        affiliation=affil,
                        clinvar_submitter_id=clinvar_submitter_id,
                    )
                for i, name in enumerate(coordinator_names):
                    # If email is is less than name list, the name will be added
                    # without any email fields.
                    if len(coordinator_emails) > i:
                        Coordinator.objects.create(
                            affiliation=affil,
                            coordinator_name=name,
                            coordinator_email=coordinator_emails[i],
                        )
                    else:
                        Coordinator.objects.create(
                            affiliation=affil,
                            coordinator_name=coordinator_names[i],
                        )
