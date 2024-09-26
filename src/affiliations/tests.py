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


class TestInvalidAffilCreateForm(TestCase):
    """A test class for testing validation error on Affiliation ID"""

    @classmethod
    def test_invalid_affil_creation(cls):
        """Attempting to seed the test database with some test data"""

        cls.invalid_affil_id_affiliation = {
            "affiliation_id": 2,
            "expert_panel_id": 40000,
            "full_name": "Invalid Affil ID Affiliation",
            "short_name": "Invalid Affil ID",
            "status": "Retired",
            "type": "GCEP",
            "clinical_domain_working_group": "Kidney Disease",
            "members": "Chikorita, Cyndaquil, Totodile",
        }
        cls.invalid_affil_id_affil = Affiliation.objects.create(
            **cls.invalid_affil_id_affiliation
        )

    @mock.patch("affiliations.admin.AffiliationForm.add_error")
    def test_response(self, mock_add_error):
        """Make sure we are triggering the add_error function in clean method"""
        invalid_affil = AffiliationForm(self.invalid_affil_id_affil)
        invalid_affil.cleaned_data = self.invalid_affil_id_affiliation
        invalid_affil.clean()
        calls = [
            mock.call(
                "affiliation_id",
                ValidationError(
                    "Valid Affiliation ID's should be in the 10000 number range. "
                    "Please include a valid Affiliation ID."
                ),
            ),
            mock.call(
                None,
                ValidationError("The Affiliation ID and Expert Panel ID do not match."),
            ),
        ]
        mock_add_error.assert_has_calls(calls)


class TestInvalidGCEPCreateForm(TestCase):
    """A test class for testing validation error on GCEP ID"""

    @classmethod
    def test_invalid_gcep_creation(cls):
        """Attempting to seed the test database with some test data"""

        cls.invalid_gcep_id_affiliation = {
            "affiliation_id": 10000,
            "expert_panel_id": 30000,
            "full_name": "Invalid GCEP ID Affiliation",
            "short_name": "Invalid GCEP ID",
            "status": "Retired",
            "type": "GCEP",
            "clinical_domain_working_group": "Kidney Disease",
            "members": "Chikorita, Cyndaquil, Totodile",
        }

        cls.invalid_gcep_id_affil = Affiliation.objects.create(
            **cls.invalid_gcep_id_affiliation
        )

    @mock.patch("affiliations.admin.AffiliationForm.add_error")
    def test_response(self, mock_add_error):
        """Make sure we are triggering the add_error function in clean method"""
        gcep_affil = AffiliationForm(self.invalid_gcep_id_affil)
        gcep_affil.cleaned_data = self.invalid_gcep_id_affiliation
        gcep_affil.clean()
        calls = [
            mock.call(
                "expert_panel_id",
                ValidationError(
                    "Valid GCEP ID's should be in the 40000 number range. "
                    "Please include a valid Expert Panel ID."
                ),
            )
        ]
        mock_add_error.assert_has_calls(calls)


class TestInvalidVCEPCreateForm(TestCase):
    """A test class for testing validation error on VCEP ID"""

    @classmethod
    def test_invalid_vcep_creation(cls):
        """Attempting to seed the test database with some test data, then make
        sure we are triggering the ValidationError"""

        cls.invalid_vcep_id_affiliation = {
            "affiliation_id": 10000,
            "expert_panel_id": 60000,
            "full_name": "Invalid VCEP ID Affiliation",
            "short_name": "Invalid VCEP ID",
            "status": "Retired",
            "type": "VCEP",
            "clinical_domain_working_group": "Kidney Disease",
            "members": "Chikorita, Cyndaquil, Totodile",
        }

        cls.invalid_vcep_id_affil = Affiliation.objects.create(
            **cls.invalid_vcep_id_affiliation
        )

    @mock.patch("affiliations.admin.AffiliationForm.add_error")
    def test_response(self, mock_add_error):
        """Make sure we are triggering the add_error function in clean method"""
        vcep_affil = AffiliationForm(self.invalid_vcep_id_affil)
        vcep_affil.cleaned_data = self.invalid_vcep_id_affiliation
        vcep_affil.clean()
        calls = [
            mock.call(
                "expert_panel_id",
                ValidationError(
                    "Valid VCEP ID's should be in the  50000 number range. "
                    "Please include a valid Expert Panel ID."
                ),
            )
        ]
        mock_add_error.assert_has_calls(calls)


class TestInvalidTypeAndIDCreateForm(TestCase):
    """A test class for testing validation error on Independent Curation Group
    type with a expert_panel_id value"""

    @classmethod
    def test_invalid_type_and_id_creation(cls):
        """Attempting to seed the test database with some test data, then make
        sure we are triggering the ValidationError"""

        cls.invalid_type_and_id_affiliation = {
            "affiliation_id": 10001,
            "expert_panel_id": 60000,
            "full_name": "Invalid Type with ID Affiliation",
            "short_name": "Invalid Type with ID",
            "status": "Retired",
            "type": "INDEPENDENT_CURATION",
            "clinical_domain_working_group": "Kidney Disease",
            "members": "Chikorita, Cyndaquil, Totodile",
        }

        cls.invalid_type_and_id_affil = Affiliation.objects.create(
            **cls.invalid_type_and_id_affiliation
        )

    @mock.patch("affiliations.admin.AffiliationForm.add_error")
    def test_response(self, mock_add_error):
        """Make sure we are triggering the add_error function in clean method"""
        invalid_type = AffiliationForm(self.invalid_type_and_id_affil)
        invalid_type.cleaned_data = self.invalid_type_and_id_affiliation
        invalid_type.clean()
        calls = [
            mock.call(
                "expert_panel_id",
                ValidationError(
                    "If type Independent Curation Group or SC-VCEP is selected, "
                    "Expert Panel ID must be left blank."
                ),
            )
        ]
        mock_add_error.assert_has_calls(calls)


class TestInvalidTypeAndIDCreateFormSCVCEP(TestCase):
    """A test class for testing validation error on Independent Curation Group
    type with a expert_panel_id value"""

    @classmethod
    def test_invalid_type_and_id_creation(cls):
        """Attempting to seed the test database with some test data, then make
        sure we are triggering the ValidationError"""

        cls.invalid_type_and_id_affiliation = {
            "affiliation_id": 10001,
            "expert_panel_id": 60000,
            "full_name": "Invalid Type with ID Affiliation",
            "short_name": "Invalid Type with ID",
            "status": "Retired",
            "type": "SC_VCEP",
            "clinical_domain_working_group": "Kidney Disease",
            "members": "Chikorita, Cyndaquil, Totodile",
        }

        cls.invalid_type_and_id_affil = Affiliation.objects.create(
            **cls.invalid_type_and_id_affiliation
        )

    @mock.patch("affiliations.admin.AffiliationForm.add_error")
    def test_response(self, mock_add_error):
        """Make sure we are triggering the add_error function in clean method"""
        invalid_type = AffiliationForm(self.invalid_type_and_id_affil)
        invalid_type.cleaned_data = self.invalid_type_and_id_affiliation
        invalid_type.clean()
        calls = [
            mock.call(
                "expert_panel_id",
                ValidationError(
                    "If type Independent Curation Group or SC-VCEP is selected, "
                    "Expert Panel ID must be left blank."
                ),
            )
        ]
        mock_add_error.assert_has_calls(calls)


class TestInvalidAffilandExpertPanelMatchCreateForm(TestCase):
    """A test class for testing validation error on Affiliation ID
    and Expert Panel match."""

    @classmethod
    def test_invalid_matching_ids_creation(cls):
        """Attempting to seed the test database with some test data, then make
        sure we are triggering the ValidationError"""

        cls.invalid_matching_ids_affiliation = {
            "affiliation_id": 14285,
            "expert_panel_id": 54284,
            "full_name": "Affil and EP ID Don't Match",
            "short_name": "Invalid Matching IDs",
            "status": "Active",
            "type": "VCEP",
            "clinical_domain_working_group": "Somatic Cancer",
            "members": "Piplup, Toxicroak, Weavile",
        }

        cls.invalid_matching_ids_affil = Affiliation.objects.create(
            **cls.invalid_matching_ids_affiliation
        )

    @mock.patch("affiliations.admin.AffiliationForm.add_error")
    def test_response(self, mock_add_error):
        """Make sure we are triggering the add_error function in clean method"""
        invalid_matching_ids = AffiliationForm(self.invalid_matching_ids_affil)
        invalid_matching_ids.cleaned_data = self.invalid_matching_ids_affiliation
        invalid_matching_ids.clean()
        calls = [
            mock.call(
                None,
                ValidationError("The Affiliation ID and Expert Panel ID do not match."),
            )
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
