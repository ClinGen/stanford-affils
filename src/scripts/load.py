import csv
import os
from affiliations.models import Affiliation, Submitter


def run():
    file = open(
        "/Users/gabriellasanchez/Desktop/repos/stanford-affils/src/scripts/test_affils.csv")
    csv_reader = csv.DictReader(file)

    Affiliation.objects.all().delete()

    for row in csv_reader:
        external_full_name = row["Affiliation Full Name"]
        affil_id = row["AffiliationID"]
        #  coordinator_name = row["Coordinator(s)"] # will need to extract multiple names
        #  coordinator_email = row["Email"] # will need to extract multiple emails
        clinvar_submitter_id = row["Submitter ID"]
        vcep_ep_id = row["VCEP Affiliation ID"]
        vcep_full_name = row["VCEP Affiliation Name"]
        gcep_ep_id = row["GCEP Affiliation ID"]
        gcep_full_name = row["GCEP Affiliation Name"]
        status = row["Status"]
        # CDWG

        if gcep_ep_id:
            affil = Affiliation.objects.create(
                affiliation_id=affil_id,
                expert_panel_id=gcep_ep_id,
                type="GCEP",
                full_name=gcep_full_name,
                status=status,
                )
            if clinvar_submitter_id != "":
                Submitter.objects.create(
                    affiliation=affil,
                    clinvar_submitter_id=clinvar_submitter_id,
                    )
        if vcep_ep_id:
            if "SC-VCEP" in vcep_full_name:
                affil = Affiliation.objects.create(
                    affiliation_id=affil_id,
                    expert_panel_id=vcep_ep_id,
                    type="SC_VCEP",
                    full_name=vcep_full_name,
                    status=status,
                    )
                if clinvar_submitter_id != "":
                    Submitter.objects.create(
                        affiliation=affil,
                        clinvar_submitter_id=clinvar_submitter_id,
                        )
            else:
                affil = Affiliation.objects.create(
                    affiliation_id=affil_id,
                    expert_panel_id=vcep_ep_id,
                    type="VCEP",
                    full_name=vcep_full_name,
                    status=status,
                    )
                if clinvar_submitter_id != "":
                    Submitter.objects.create(
                        affiliation=affil,
                        clinvar_submitter_id=clinvar_submitter_id,
                        )
        if not gcep_ep_id and not vcep_ep_id:
            affil = Affiliation.objects.create(
                affiliation_id=affil_id,
                expert_panel_id=None,
                type="INDEPENDENT_CURATION",
                full_name=external_full_name,
                status=status,
                )
            if clinvar_submitter_id != "":
                Submitter.objects.create(
                    affiliation=affil,
                    clinvar_submitter_id=clinvar_submitter_id,
                    )
