"""Tests for the affiliations service."""

# Third-party dependencies:
from unittest import mock
from django.test import TestCase

from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

# In-house code:
from affiliations.views import AffiliationsList
from affiliations.views import AffiliationsDetail
from affiliations.models import Affiliation, Coordinator, Approver, Submitter

from affiliations.admin import AffiliationForm


class AffiliationsViewsBaseTestCase(TestCase):
    """A base test class with setup for testing affiliations views."""

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        """Seed the test database with some test data."""
        cls.success_affiliation = {
            "affiliation_id": 10000,
            "expert_panel_id": 40000,
            "full_name": "Test Success Result Affil",
            "short_name": "Successful",
            "status": "Inactive",
            "type": "Gene Curation Expert Panel",
            "clinical_domain_working_group": "Neurodevelopmental Disorders",
            "members": "Bulbasaur, Charmander, Squirtle",
        }
        cls.expected_success_affiliation = {
            **cls.success_affiliation,
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
            "clinical_domain_working_group": "Hoenn League",
            "members": "Treecko, Torchic, Mudkip",
        }
        cls.expected_hoenn_affiliation = {
            **cls.hoenn_affiliation,
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
            "clinical_domain_working_group": ["Kidney Disease"],
            "members": "Chikorita, Cyndaquil, Totodile",
        }

        cls.cleaned_user_input_ids_affiliation = {
            "affiliation_id": 10000,
            "expert_panel_id": None,
            "full_name": "Invalid Type with ID Affiliation",
            "short_name": "Invalid Type with ID",
            "status": "Retired",
            "type": "SC_VCEP",
            "clinical_domain_working_group": ["Kidney Disease"],
            "members": "Chikorita, Cyndaquil, Totodile",
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
        cls.out_of_range_id_affiliation_base = {
            # Creating an affil in the DB with incorrect information. change this.
            "affiliation_id": 19999,
            "expert_panel_id": 59999,
            "full_name": "Max Affiliation ID",
            "short_name": "Max Affil ID",
            "status": "Retired",
            "type": "VCEP",
            "clinical_domain_working_group": ["Kidney Disease"],
            "members": "Chikorita, Cyndaquil, Totodile",
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


class AffiliationsListTestCase(AffiliationsViewsBaseTestCase):
    """Test the affiliations list view."""

    def test_should_be_able_to_view_list_of_affiliations(self):
        """Make sure we are able to view our list of affiliations."""
        factory = APIRequestFactory()
        view = AffiliationsList.as_view()
        request = factory.get("/")
        response = view(request)
        self.assertDictEqual(
            response.data[0],
            self.expected_success_affiliation,
        )
        self.assertDictEqual(
            response.data[1],
            self.expected_hoenn_affiliation,
        )


class AffiliationsDetailTestCase(AffiliationsViewsBaseTestCase):
    """Test the affiliations details view."""

    def test_should_be_able_to_view_single_affiliation_detail(self):
        """Make sure we are able to view a single affiliation's details."""
        factory = APIRequestFactory()
        view = AffiliationsDetail.as_view()
        primary_key = 1
        request = factory.get(f"/{primary_key}")
        response = view(request, pk=primary_key)
        self.assertDictEqual(response.data, self.expected_success_affiliation)
        primary_key = 2
        request = factory.get(f"/{primary_key}")
        response = view(request, pk=primary_key)
        self.assertDictEqual(response.data, self.expected_hoenn_affiliation)
