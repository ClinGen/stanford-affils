"""Tests for the affiliations service."""

# Third-party dependencies:
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from affiliations.views import AffiliationsList
from affiliations.views import AffiliationsDetail
from affiliations.models import Affiliation


class AffiliationsViewsBaseTestCase(TestCase):
    """A base test class with setup for testing affiliations views."""

    @classmethod
    def setUpTestData(cls):
        """Seed the test database with some test data."""
        cls.kanto_affiliation = {
            "affiliation_id": 1,
            "name": "Kanto Pokémon",
            "coordinator": "Professor Oak",
            "status": "Inactive",
            "type": "Cool",
            "family": "Indigo League",
            "members": "Bulbasaur, Charmander, Squirtle",
            "approvers": "Mew",
            "clinvar_submitter_ids": "11, 22, 33",
        }
        cls.johto_affiliation = {
            "affiliation_id": 2,
            "name": "Johto Pokémon",
            "coordinator": "Professor Elm",
            "status": "Retired",
            "type": "Cool",
            "family": "Johto League",
            "members": "Chikorita, Cyndaquil, Totodile",
            "approvers": "Celebi",
            "clinvar_submitter_ids": "44, 55, 66",
        }
        cls.hoenn_affiliation = {
            "affiliation_id": 3,
            "name": "Hoenn Pokémon",
            "coordinator": "Professor Birch",
            "status": "Active",
            "type": "Cool",
            "family": "Hoenn League",
            "members": "Treecko, Torchic, Mudkip",
            "approvers": "Groudon, Kyogre",
            "clinvar_submitter_ids": "77, 88, 99",
        }
        Affiliation.objects.create(**cls.kanto_affiliation)
        Affiliation.objects.create(**cls.johto_affiliation)
        Affiliation.objects.create(**cls.hoenn_affiliation)


class AffiliationsListTestCase(AffiliationsViewsBaseTestCase):
    """Test the affiliations list view."""

    def test_should_be_able_to_view_list_of_affiliations(self):
        """Make sure we are able to view our list of affiliations."""
        factory = APIRequestFactory()
        view = AffiliationsList.as_view()
        request = factory.get("/")
        response = view(request)
        self.assertEqual(
            response.data,
            [self.kanto_affiliation, self.johto_affiliation, self.hoenn_affiliation],
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
        self.assertEqual(response.data, self.kanto_affiliation)
        primary_key = 2
        request = factory.get(f"/{primary_key}")
        response = view(request, pk=primary_key)
        self.assertEqual(response.data, self.johto_affiliation)
        primary_key = 3
        request = factory.get(f"/{primary_key}")
        response = view(request, pk=primary_key)
        self.assertEqual(response.data, self.hoenn_affiliation)
