"""Tests for the affiliations service."""

# Third-party dependencies:
from unittest import mock
from django.test import TestCase

from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory, APITestCase

from rest_framework_api_key.models import APIKey

# In-house code:
from affiliations.views import AffiliationsList
from affiliations.views import AffiliationsDetail
from affiliations.models import (
    Affiliation,
    Coordinator,
    Approver,
    Submitter,
    ClinicalDomainWorkingGroup,
)

from affiliations.admin import AffiliationForm


class AffiliationsViewsBaseTestCase(APITestCase):
    """A base test class with setup for testing affiliations views."""

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        """Seed the test database with some test data."""

        cdwg1, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            code="HEARING_LOSS", defaults={"name": "Hearing Loss"}
        )
        cdwg2, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            code="RHEUMA_AUTO_DISEASE",
            defaults={"name": "Rheumatologic Autoimmune Disease"},
        )
        cls.success_affiliation = {
            "affiliation_id": 10000,
            "expert_panel_id": 40000,
            "full_name": "Test Success Result Affil",
            "short_name": "Successful",
            "status": "Inactive",
            "type": "GCEP",
            "members": "Bulbasaur, Charmander, Squirtle",
            "is_deleted": False,
            "clinical_domain_working_group": cdwg1,
        }
        cls.expected_success_affiliation = {
            **cls.success_affiliation,
            "clinical_domain_working_group": cdwg1.id,
            "coordinators": [
                {
                    "coordinator_name": "Professor Oak",
                    "coordinator_email": "ProfessorOak@email.com",
                },
            ],
            "approvers": [
                {
                    "approver_name": "Mew",
                },
            ],
            "clinvar_submitter_ids": [
                {
                    "clinvar_submitter_id": "11",
                },
                {
                    "clinvar_submitter_id": "22",
                },
                {
                    "clinvar_submitter_id": "33",
                },
            ],
        }

        cls.hoenn_affiliation = {
            "affiliation_id": 3,
            "expert_panel_id": 2003,
            "full_name": "Hoenn Pokémon",
            "short_name": "Hoenn",
            "status": "Active",
            "type": "Cool",
            "members": "Treecko, Torchic, Mudkip",
            "is_deleted": False,
            "clinical_domain_working_group": cdwg2,
        }
        cls.expected_hoenn_affiliation = {
            **cls.hoenn_affiliation,
            "clinical_domain_working_group": cdwg2.id,
            "coordinators": [
                {
                    "coordinator_name": "Professor Birch",
                    "coordinator_email": "ProfessorBirch@email.com",
                }
            ],
            "approvers": [
                {
                    "approver_name": "Groudon",
                },
                {
                    "approver_name": "Kyogre",
                },
            ],
            "clinvar_submitter_ids": [
                {
                    "clinvar_submitter_id": "77",
                },
                {
                    "clinvar_submitter_id": "88",
                },
                {
                    "clinvar_submitter_id": "99",
                },
            ],
        }

        success_affil = Affiliation.objects.create(**cls.success_affiliation)
        Coordinator.objects.create(
            affiliation=success_affil,
            coordinator_name="Professor Oak",
            coordinator_email="ProfessorOak@email.com",
        )
        Approver.objects.create(
            affiliation=success_affil,
            approver_name="Mew",
        )
        Submitter.objects.create(
            affiliation=success_affil,
            clinvar_submitter_id="11",
        )
        Submitter.objects.create(
            affiliation=success_affil,
            clinvar_submitter_id="22",
        )
        Submitter.objects.create(
            affiliation=success_affil,
            clinvar_submitter_id="33",
        )

        hoenn_affil = Affiliation.objects.create(**cls.hoenn_affiliation)
        Coordinator.objects.create(
            affiliation=hoenn_affil,
            coordinator_name="Professor Birch",
            coordinator_email="ProfessorBirch@email.com",
        )
        Approver.objects.create(
            affiliation=hoenn_affil,
            approver_name="Groudon",
        )
        Approver.objects.create(
            affiliation=hoenn_affil,
            approver_name="Kyogre",
        )
        Submitter.objects.create(
            affiliation=hoenn_affil,
            clinvar_submitter_id="77",
        )
        Submitter.objects.create(
            affiliation=hoenn_affil,
            clinvar_submitter_id="88",
        )
        Submitter.objects.create(
            affiliation=hoenn_affil,
            clinvar_submitter_id="99",
        )

    def test_should_be_able_to_view_list_of_affiliations(self):
        """Make sure we are able to view our list of affiliations."""
        factory = APIRequestFactory()
        view = AffiliationsList.as_view()
        request = factory.get("/database_list/")
        response = view(request)
        self.assertDictEqual(
            response.data[0],
            self.expected_success_affiliation,
        )
        self.assertDictEqual(
            response.data[1],
            self.expected_hoenn_affiliation,
        )

    def test_should_be_able_to_view_single_affiliation_detail(self):
        """Make sure we are able to view a single affiliation's details."""
        factory = APIRequestFactory()
        view = AffiliationsDetail.as_view()
        primary_key = 1
        request = factory.get(f"/database_list/{primary_key}")
        response = view(request, pk=primary_key)
        self.assertEqual(response.status_code, 200)

        self.assertDictEqual(response.data, self.expected_success_affiliation)
        primary_key = 2
        request = factory.get(f"/database_list/{primary_key}")
        response = view(request, pk=primary_key)
        self.assertDictEqual(response.data, self.expected_hoenn_affiliation)

    def test_detail_affiliation_json_call(self):
        """Make sure the API response of a single affiliation is returned
        in the original JSON format ."""
        _, key = APIKey.objects.create_key(name="my-remote-service")
        auth_headers = {"HTTP_X_API_KEY": key}
        response = self.client.get(
            "/api/affiliation_detail/?affil_id=10000", **auth_headers
        )
        self.assertEqual(
            response.json(),
            [
                {
                    "affiliation_id": "10000",
                    "affiliation_fullname": "Test Success Result Affil",
                    "subgroups": {
                        "gcep": {
                            "id": "40000",
                            "fullname": "Test Success Result Affil",
                        }
                    },
                    "approver": ["Mew"],
                }
            ],
        )
        self.assertEqual(response.status_code, 200)

    def test_list_affiliation_json_call(self):
        """Make sure the API response of all the affiliations in the db is
        returned in the original JSON format ."""
        _, key = APIKey.objects.create_key(name="my-remote-service")
        auth_headers = {"HTTP_X_API_KEY": key}
        response = self.client.get("/api/affiliations_list/", **auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


class TestUserInputsIds(TestCase):
    """A test class for testing validation if a user passed in an affiliation ID
    and/or EP ID."""

    @classmethod
    def setUpTestData(cls):
        """Creating test data then test that we are overwriting the provided data."""
        cls.user_input_ids_affiliation = {
            "affiliation_id": 100001,
            "expert_panel_id": 60000,
            "full_name": "Invalid Type with ID Affiliation",
            "short_name": "Invalid Type with ID",
            "status": "Retired",
            "type": "SC_VCEP",
            "clinical_domain_working_group": 8,
            "members": "Chikorita, Cyndaquil, Totodile",
            "is_deleted": False,
        }

        cls.cleaned_user_input_ids_affiliation = {
            "affiliation_id": 10000,
            "expert_panel_id": None,
            "full_name": "Invalid Type with ID Affiliation",
            "short_name": "Invalid Type with ID",
            "status": "Retired",
            "type": "SC_VCEP",
            "clinical_domain_working_group": 8,
            "members": "Chikorita, Cyndaquil, Totodile",
            "is_deleted": False,
        }

    @mock.patch("affiliations.admin.AffiliationForm.add_error")
    def test_response(self, mock_add_error):
        """Make sure we are overwriting provided user inputs in clean method"""
        user_input_ids = AffiliationForm(self.user_input_ids_affiliation)
        user_input_ids.cleaned_data = self.cleaned_user_input_ids_affiliation
        user_input_ids.clean()
        mock_add_error.assert_not_called()


class TestAffiliationIDOutOfRange(TestCase):
    """A test class for testing validation errors if max Affil ID and VCEP ID
    are reached."""

    @classmethod
    def setUpTestData(cls):
        """Attempting to seed the test database with some test data, then test
        that the expected validation errors are triggered"""
        cdwg3, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            code="KIDNEY_DISEASE", defaults={"name": "Kidney Disease"}
        )
        cls.out_of_range_id_affiliation_base = {
            # Creating an affil in the DB with incorrect information. change this.
            "affiliation_id": 19999,
            "expert_panel_id": 59999,
            "full_name": "Max Affiliation ID",
            "short_name": "Max Affil ID",
            "status": "Retired",
            "type": "VCEP",
            "clinical_domain_working_group": cdwg3,
            "members": "Chikorita, Cyndaquil, Totodile",
            "is_deleted": False,
        }

        cls.out_of_range_affil = Affiliation.objects.create(
            **cls.out_of_range_id_affiliation_base
        )

        cls.out_of_range_id_affiliation = {
            **cls.out_of_range_id_affiliation_base,
        }

    @mock.patch("affiliations.admin.AffiliationForm.add_error")
    def test_response(self, mock_add_error):
        """Make sure expected validation errors are triggered in clean method"""
        out_of_range = AffiliationForm(self.out_of_range_affil)
        out_of_range.cleaned_data = self.out_of_range_id_affiliation
        out_of_range.clean()
        calls = [
            mock.call(
                None,
                ValidationError("Affiliation ID out of range. Contact administrator."),
            ),
            mock.call(
                None,
                ValidationError("VCEP ID out of range. Contact administrator."),
            ),
        ]
        mock_add_error.assert_has_calls(calls)


class TestCDWGModel(TestCase):
    """A test class for testing validation errors dealing with CDWGs."""

    def test_duplicate_code_fails(self):
        """Make sure expected validation errors are triggered when duplicate
        CDWGs are created."""
        ClinicalDomainWorkingGroup.objects.create(code="EYE", name="Eye Disorders")
        with self.assertRaises(Exception):
            ClinicalDomainWorkingGroup.objects.create(
                code="EYE", name="Duplicate Eye Disorders"
            )

    def test_affiliation_missing_cdwg_raises_error(self):
        """Make sure expected validation errors are triggered if an affiliation
        is created without a CDWG."""
        with self.assertRaises(Exception):
            Affiliation.objects.create(
                affiliation_id=99999,
                expert_panel_id=88888,
                full_name="Missing CDWG Affil",
                short_name="Missing",
                status="Active",
                type="GCEP",
                members="",
                is_deleted=False,
            )
