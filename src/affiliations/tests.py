"""Tests for the affiliations service."""

# Third-party dependencies:
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from affiliations.views import AffiliationsList
from affiliations.views import AffiliationsDetail
from affiliations.models import Affiliation, Coordinator, Approver, Submitter


class AffiliationsViewsBaseTestCase(TestCase):
    """A base test class with setup for testing affiliations views."""

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        """Seed the test database with some test data."""
        cls.kanto_affiliation = {
            "affiliation_id": 1,
            "full_name": "Kanto Pokémon",
            "abbreviated_name": "Kanto",
            "status": "Inactive",
            "type": "Cool",
            "clinical_domain_working_group": "Indigo League",
            "members": "Bulbasaur, Charmander, Squirtle",
        }
        cls.expected_kanto_affiliation = {
            **cls.kanto_affiliation,
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
        cls.johto_affiliation = {
            "affiliation_id": 2,
            "full_name": "Johto Pokémon",
            "abbreviated_name": "Johto",
            "status": "Retired",
            "type": "Cool",
            "clinical_domain_working_group": "Johto League",
            "members": "Chikorita, Cyndaquil, Totodile",
        }
        cls.expected_johto_affiliation = {
            **cls.johto_affiliation,
            "coordinators": [
                {
                    "coordinator_name": "Professor Elm",
                    "coordinator_email": "ProfessorElm@email.com",
                },
            ],
            "approvers": [
                {
                    "approver_name": "Celebi",
                },
            ],
            "clinvar_submitter_ids": [
                {
                    "clinvar_submitter_id": "44",
                },
                {
                    "clinvar_submitter_id": "55",
                },
                {
                    "clinvar_submitter_id": "66",
                },
            ],
        }
        cls.hoenn_affiliation = {
            "affiliation_id": 3,
            "full_name": "Hoenn Pokémon",
            "abbreviated_name": "Hoenn",
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

        kanto_affil = Affiliation.objects.create(**cls.kanto_affiliation)
        Coordinator.objects.create(
            affiliation=kanto_affil,
            coordinator_name="Professor Oak",
            coordinator_email="ProfessorOak@email.com",
        )
        Approver.objects.create(
            affiliation=kanto_affil,
            approver_name="Mew",
        )
        Submitter.objects.create(
            affiliation=kanto_affil,
            clinvar_submitter_id="11",
        )
        Submitter.objects.create(
            affiliation=kanto_affil,
            clinvar_submitter_id="22",
        )
        Submitter.objects.create(
            affiliation=kanto_affil,
            clinvar_submitter_id="33",
        )
        johto_affil = Affiliation.objects.create(**cls.johto_affiliation)
        Coordinator.objects.create(
            affiliation=johto_affil,
            coordinator_name="Professor Elm",
            coordinator_email="ProfessorElm@email.com",
        )
        Approver.objects.create(
            affiliation=johto_affil,
            approver_name="Celebi",
        )
        Submitter.objects.create(
            affiliation=johto_affil,
            clinvar_submitter_id="44",
        )
        Submitter.objects.create(
            affiliation=johto_affil,
            clinvar_submitter_id="55",
        )
        Submitter.objects.create(
            affiliation=johto_affil,
            clinvar_submitter_id="66",
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
            self.expected_kanto_affiliation,
        )
        self.assertDictEqual(
            response.data[1],
            self.expected_johto_affiliation,
        )
        self.assertDictEqual(
            response.data[2],
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
        self.assertDictEqual(response.data, self.expected_kanto_affiliation)
        primary_key = 2
        request = factory.get(f"/{primary_key}")
        response = view(request, pk=primary_key)
        self.assertEqual(response.data, self.expected_johto_affiliation)
        primary_key = 3
        request = factory.get(f"/{primary_key}")
        response = view(request, pk=primary_key)
        self.assertEqual(response.data, self.expected_hoenn_affiliation)
