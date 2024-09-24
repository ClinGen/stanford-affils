import csv
import os
from affiliations.models import Affiliation, Submitter, Coordinator


def run():
    file = open(
        "/Users/gabriellasanchez/Desktop/repos/stanford-affils/src/scripts/test_affils.csv")
    csv_reader = csv.DictReader(file)

    Affiliation.objects.all().delete()

    for row in csv_reader:
        external_full_name = row["Affiliation Full Name"]
        affil_id = row["AffiliationID"]
        coordinator_name = row["Coordinator(s)"].strip()
        coordinator_email = row["Email"].strip()
        clinvar_submitter_id = row["Submitter ID"]
        vcep_ep_id = row["VCEP Affiliation ID"]
        vcep_full_name = row["VCEP Affiliation Name"]
        gcep_ep_id = row["GCEP Affiliation ID"]
        gcep_full_name = row["GCEP Affiliation Name"]
        status = row["Status"]
        # cdwg = row["CDWG"]

        coordinator_names = coordinator_name.split(",")
        coordinator_emails = coordinator_email.split(",")

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
            if coordinator_names or coordinator_emails:
                for i in range(len(coordinator_names)):
                    # If email is is less than name list, the name will be added
                    # without any email fields.
                    if len(coordinator_emails) > i:
                        Coordinator.objects.create(
                            affiliation=affil,
                            coordinator_name=coordinator_names[i],
                            coordinator_email=coordinator_emails[i],
                        )
                    else:
                        Coordinator.objects.create(
                            affiliation=affil,
                            coordinator_name=coordinator_names[i],
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
                if coordinator_names or coordinator_emails:
                    for i in range(len(coordinator_names)):
                        # If email is is less than name list, the name will be added
                        # without any email fields.
                        if len(coordinator_emails) > i:
                            Coordinator.objects.create(
                                affiliation=affil,
                                coordinator_name=coordinator_names[i],
                                coordinator_email=coordinator_emails[i],
                            )
                        else:
                            Coordinator.objects.create(
                                affiliation=affil,
                                coordinator_name=coordinator_names[i],
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
                if coordinator_names or coordinator_emails:
                    for i in range(len(coordinator_names)):
                        # If email is is less than name list, the name will be added
                        # without any email fields.
                        if len(coordinator_emails) > i:
                            Coordinator.objects.create(
                                affiliation=affil,
                                coordinator_name=coordinator_names[i],
                                coordinator_email=coordinator_emails[i],
                            )
                        else:
                            Coordinator.objects.create(
                                affiliation=affil,
                                coordinator_name=coordinator_names[i],
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
            if coordinator_names or coordinator_emails:
                for i in range(len(coordinator_names)):
                    # If email is is less than name list, the name will be added
                    # without any email fields.
                    if len(coordinator_emails) > i:

                        Coordinator.objects.create(
                            affiliation=affil,
                            coordinator_name=coordinator_names[i],
                            coordinator_email=coordinator_emails[i],
                        )
                    else:
                        Coordinator.objects.create(
                            affiliation=affil,
                            coordinator_name=coordinator_names[i],
                        )
