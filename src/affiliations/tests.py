"""Tests for the affiliations service."""

# Third-party dependencies:
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

# In-house code:
from affiliations.models import (
    Affiliation,
    Coordinator,
    Approver,
    Submitter,
    ClinicalDomainWorkingGroup,
    CustomAPIKey,
)

from affiliations.serializers import AffiliationSerializer
from affiliations.utils import (
    generate_next_affiliation_id,
    set_expert_panel_id,
    validate_cdwg_matches_type,
)
from affiliations.permissions import HasWriteAccess


class AffiliationsViewsBaseTestCase(APITestCase):
    """A base test class with setup for testing affiliations views."""

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        """Seed the test database with some test data."""
        _, cls.api_key = CustomAPIKey.objects.create_key(
            name="test-service", can_write=True
        )
        cdwg1, _ = ClinicalDomainWorkingGroup.objects.get_or_create(name="Hearing Loss")

        cls.success_affiliation = {
            "full_name": "Test Success Result Affil",
            "short_name": "Successful",
            "status": "INACTIVE",
            "type": "GCEP",
            "members": "Bulbasaur, Charmander, Squirtle",
            "is_deleted": False,
            "clinical_domain_working_group": cdwg1,
        }
        # Pass data through custom clean functions to generate affil and EP ID
        generate_next_affiliation_id(cls.success_affiliation)
        set_expert_panel_id(cls.success_affiliation)
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
        Submitter.objects.bulk_create(
            [
                Submitter(affiliation=success_affil, clinvar_submitter_id=id)
                for id in ["11", "22", "33"]
            ]
        )

        cls.cdwg2 = ClinicalDomainWorkingGroup.objects.create(
            name="Hemostasis/Thrombosis"
        )
        cls.create_data = {
            "full_name": "Test VCEP",
            "type": "VCEP",
            "status": "ACTIVE",
            "clinical_domain_working_group": cls.cdwg2.id,
        }

    def test_should_be_able_to_view_list_of_affiliations(self):
        """Make sure we are able to view our list of affiliations."""
        client = APIClient()
        response = client.get("/api/database_list/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        returned_names = {affil["full_name"] for affil in response.data}
        self.assertIn("Test Success Result Affil", returned_names)

    def test_should_be_able_to_view_single_affiliation_detail(self):
        """Make sure we are able to view a single affiliation's details."""
        client = APIClient()
        affil = Affiliation.objects.get(full_name="Test Success Result Affil")

        response = client.get(f"/api/database_list/{affil.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["full_name"], self.success_affiliation["full_name"]
        )

    def test_detail_affiliation_json_call(self):
        """Make sure the API response of a single affiliation is returned
        in the original JSON format ."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get("/api/affiliation_detail/?affil_id=10000")
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
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get("/api/affiliations_list/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_affiliation__success(self):
        """Test successful creation of affiliation via POST API with valid data."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.post(
            "/api/affiliation/create/",
            self.create_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("affiliation_id", response.data)
        self.assertIn("expert_panel_id", response.data)

    def test_create_affiliation_missing_required_fields(self):
        """Test that missing required fields in POST request returns 400 and error messages."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.post("/api/affiliation/create/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("full_name", response.data["details"])
        self.assertIn("type", response.data["details"])


class TestCDWGModel(TestCase):
    """A test class for testing validation errors dealing with CDWGs."""

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


class AffiliationSerializerTest(TestCase):
    """Tests for the AffiliationSerializer create and validation logic."""

    @classmethod
    def setUpTestData(cls):
        """Set up a CDWG for serializer tests."""
        cls.cdwg, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            name="Somatic Cancer"
        )
        cls.affiliation = Affiliation.objects.create(
            affiliation_id=10000,
            expert_panel_id=40000,
            full_name="Base Name",
            short_name="BaseShort",
            status="ACTIVE",
            type="SC_VCEP",
            members="Initial Name",
            is_deleted=False,
            clinical_domain_working_group=cls.cdwg,
        )

    def test_serializer_create_affiliation__success(self):
        """Test successful serialization and creation of an SC_VCEP affiliation."""
        payload = {
            "full_name": "Test SC_VCEP",
            "type": "SC_VCEP",
            "status": "ACTIVE",
            "clinical_domain_working_group": self.cdwg.id,
        }
        serializer = AffiliationSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertIsInstance(instance, Affiliation)
        self.assertGreaterEqual(instance.expert_panel_id, 50000)

    def test_serializer_fails_with_missing_required_fields(self):
        """Test serializer validation fails when required fields are missing."""
        data = {
            "status": "ACTIVE",
            "type": "SC_VCEP",
            "clinical_domain_working_group": self.cdwg.id,
            # Missing 'full_name'
        }
        serializer = AffiliationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("full_name", serializer.errors)

    def test_serializer_update_success(self):
        """Test to successfully update an affiliation via serializer."""
        data = {
            "full_name": "Changed Name",
            "status": "INACTIVE",
            "coordinators": [
                {
                    "coordinator_name": "Prof. Elm",
                    "coordinator_email": "elm@email.com",
                }
            ],
        }
        serializer = AffiliationSerializer(
            instance=self.affiliation, data=data, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_instance = serializer.save()

        self.assertEqual(updated_instance.full_name, "Changed Name")
        self.assertEqual(updated_instance.coordinators.count(), 1)

    def test_serializer_immutable_field_error(self):
        """Test to attempt to change immutable field and expected validation errors."""
        data = {"type": "VCEP"}
        serializer = AffiliationSerializer(
            instance=self.affiliation, data=data, partial=True
        )
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError) as ctx:
            serializer.save()
        self.assertIn("type", ctx.exception.detail)


class AffiliationUtilsTest(TestCase):
    """Tests for affiliation helper utility functions."""

    @classmethod
    def setUpTestData(cls):
        """Set up test CDWG used across utility tests."""
        cls.cdwg, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            name="Somatic Cancer"
        )

    def test_generate_next_affiliation_id(self):
        """Test that the next affiliation ID is generated and added to cleaned_data."""
        cleaned_data = {}
        generate_next_affiliation_id(cleaned_data)
        self.assertIn("affiliation_id", cleaned_data)
        self.assertGreaterEqual(cleaned_data["affiliation_id"], 10000)

    def test_set_expert_panel_id_success(self):
        """Test that a valid SC_VCEP affiliation sets the correct expert_panel_id."""
        cleaned_data = {
            "affiliation_id": 10000,
            "type": "SC_VCEP",
            "clinical_domain_working_group": self.cdwg,
        }
        set_expert_panel_id(cleaned_data)
        self.assertIn("expert_panel_id", cleaned_data)
        self.assertGreaterEqual(cleaned_data["expert_panel_id"], 50000)

    def test_validate_cdwg_matches_type_invalid_cdwg(self):
        """Test that an SC_VCEP with incorrect CDWG raises a validation error."""
        wrong_cdwg, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            name="Cardiology"
        )
        cleaned_data = {
            "affiliation_id": 10000,
            "type": "SC_VCEP",
            "clinical_domain_working_group": wrong_cdwg,
        }
        with self.assertRaises(Exception) as context:
            validate_cdwg_matches_type(cleaned_data)
        self.assertIn(
            "If type is 'Somatic Cancer Variant Curation Expert Panel'",
            str(context.exception),
        )

    def test_generate_next_affiliation_id_raises_validation_error(self):
        """Should raise ValidationError if next affiliation_id exceeds valid range."""
        Affiliation.objects.create(
            full_name="Overflow Affiliation",
            type="SC_VCEP",
            status="ACTIVE",
            clinical_domain_working_group=self.cdwg,
            affiliation_id=19999,
            expert_panel_id=49999,
        )
        cleaned_data = {}
        with self.assertRaises(ValidationError) as cm:
            generate_next_affiliation_id(cleaned_data)

        self.assertIn("Affiliation ID out of range", str(cm.exception))

    def test_missing_affiliation_id_raises_validation_error(self):
        """Should raise ValidationError when affiliation_id is missing."""
        cleaned_data = {
            "type": "SC_VCEP",
            "clinical_domain_working_group": self.cdwg,
        }

        with self.assertRaises(ValidationError) as cm:
            set_expert_panel_id(cleaned_data)

        self.assertIn("affiliation_id is required", str(cm.exception))


class TestAffiliationUpdateView(APITestCase):
    """Test cases for updating affiliations via API"""

    @classmethod
    def setUpTestData(cls):
        _, cls.api_key = CustomAPIKey.objects.create_key(
            name="test-service", can_write=True
        )
        cls.cdwg, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            name="Cardiology"
        )
        cls.affiliation = Affiliation.objects.create(
            affiliation_id=10000,
            expert_panel_id=40000,
            full_name="Original Name",
            short_name="OrigShort",
            status="active",
            type="GCEP",
            members="Dr. Oak",
            is_deleted=False,
            clinical_domain_working_group=cls.cdwg,
        )

    def test_update_affiliation_success(self):
        """Test to successfully update an affiliation via API."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)

        payload = {
            "full_name": "Updated Name",
            "short_name": "UpdatedShort",
            "status": "INACTIVE",
        }
        response = self.client.patch(
            f"/api/affiliation/update/affiliation_id/{self.affiliation.affiliation_id}/",
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.affiliation.refresh_from_db()
        self.assertEqual(self.affiliation.full_name, "Updated Name")
        self.assertEqual(self.affiliation.status, "INACTIVE")

    def test_update_affiliation_fails_on_immutable_field(self):
        """Test to attempt to update an immutable field via API."""
        payload = {"type": "VCEP"}
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.patch(
            f"/api/affiliation/update/affiliation_id/{self.affiliation.affiliation_id}/",
            data=payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data["details"])


class TestCDWGApi(APITestCase):
    """Class for CDWG API tests."""

    @classmethod
    def setUpTestData(cls):
        """Seed the test database with some test data."""
        _, cls.api_key = CustomAPIKey.objects.create_key(
            name="test-service", can_write=True
        )
        cls.cdwg1, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            name="Cardiology"
        )
        cls.cdwg2, _ = ClinicalDomainWorkingGroup.objects.get_or_create(name="Oncology")

    def test_create_cdwg_success(self):
        """Test that a new CDWG can be successfully created with valid data."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        data = {"name": "Neurology"}
        response = self.client.post(
            "/api/cdwg/create/",
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Neurology")

    def test_update_cdwg_by_id_success(self):
        """Test that a new CDWG can be successfully created with valid data."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        update_data = {"name": "Cardiology Updated"}
        response = self.client.put(
            f"/api/cdwg/id/{self.cdwg1.id}/update/",
            update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Cardiology Updated")

    def test_list_cdwgs_success(self):
        """Test that all existing CDWGs can be listed successfully."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get(
            "/api/cdwg_list/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(c["name"] == "Cardiology" for c in response.data))

    def test_get_cdwg_by_id_success(self):
        """Test that a single CDWG can be retrieved by its ID."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get(
            f"/api/cdwg_detail/id/{self.cdwg1.id}/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Cardiology")

    def test_get_cdwg_not_found(self):
        """Test that a 404 is returned when retrieving a non-existent CDWG by ID."""
        nonexistent_id = (
            ClinicalDomainWorkingGroup.objects.order_by("-id").first().id + 100
        )
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get(
            f"/api/cdwg_detail/id/{nonexistent_id}/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_cdwg_not_found(self):
        """Test that a 404 is returned when updating a non-existent CDWG."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.put(
            "/api/cdwg/999/update/",
            {"name": "Ghost"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_cdwg_duplicate_name_case_insensitive(self):
        """Test that creating a CDWG with a duplicate name (case-insensitive) fails."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        data = {"name": "cardiology"}  # existing is "Cardiology"
        response = self.client.post(
            "/api/cdwg/create/",
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data["details"])

    def test_create_cdwg_missing_name(self):
        """Test that creating a CDWG without providing a name returns a 400."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.post(
            "/api/cdwg/create/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data["details"])

    def test_get_cdwg_by_name_success(self):
        """Test that a CDWG can be retrieved successfully using its name."""
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get(
            f"/api/cdwg_detail/name/{self.cdwg2.name}/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.cdwg2.name)


class AffiliationUpdateViewTest(APITestCase):
    """Tests for updating affiliation data using either affiliation_id or expert_panel_id."""

    @classmethod
    def setUpTestData(cls):
        _, cls.api_key = CustomAPIKey.objects.create_key(
            name="test-service", can_write=True
        )

        cls.cdwg, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            name="Immunology"
        )
        cls.affiliation = Affiliation.objects.create(
            affiliation_id=10000,
            expert_panel_id=40000,
            full_name="Original Name",
            type="GCEP",
            status="ACTIVE",
            members="Misty, Brock",
            clinical_domain_working_group=cls.cdwg,
        )

    def test_update_full_name_by_affiliation_id(self):
        """Should update editable field using affiliation_id."""
        url = (
            f"/api/affiliation/update/affiliation_id/{self.affiliation.affiliation_id}/"
        )
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        data = {"full_name": "Updated Name"}
        response = self.client.patch(
            url,
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.affiliation.refresh_from_db()
        self.assertEqual(self.affiliation.full_name, "Updated Name")

    def test_update_immutable_field_fails(self):
        """Should raise error when trying to update an immutable field."""
        url = (
            f"/api/affiliation/update/affiliation_id/{self.affiliation.affiliation_id}/"
        )
        data = {"type": "VCEP"}  # Immutable
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data["details"])

    def test_404_if_both_ids_missing(self):
        """Should raise 404 if neither ID is provided."""
        url = "/api/affiliation/update/affiliation_id/"  # Invalid URL
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_404_for_invalid_expert_panel_id(self):
        """Should return 404 for non-existent expert_panel_id."""
        url = "/api/affiliation/update/expert_panel_id/99999/"
        self.client.credentials(HTTP_X_API_KEY=self.api_key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DummyView(APIView):
    """
    A dummy view to test the HasWriteAccess permission.
    """

    permission_classes = [HasWriteAccess]

    def get(self, request):  # pylint: disable=unused-argument
        """
        Handle GET requests and return a success message if permission passes.
        """
        return Response({"detail": "success"})


class HasWriteAccessTests(TestCase):
    """
    Unit tests for the HasWriteAccess custom permission class.
    """

    def setUp(self):
        """
        Set up test data for the permission tests:
        - A valid key with write access.
        - A valid key without write access.
        - An expired key.
        - A request factory for simulating API requests.
        """
        _, self.valid_key = CustomAPIKey.objects.create_key(
            name="valid-key", can_write=True
        )
        _, self.no_write_key = CustomAPIKey.objects.create_key(
            name="no-write-key", can_write=False
        )
        _, self.expired_key = CustomAPIKey.objects.create_key(
            name="expired-key", can_write=True, expiry_date=now() - timedelta(days=1)
        )
        self.factory = APIRequestFactory()

    def _make_request(self, key):
        """
        Helper method to create a GET request with the specified API key.
        Returns a simulated GET request.
        """
        return self.factory.get("/dummy-endpoint/", HTTP_X_API_KEY=key)

    def test_valid_key_with_write_access(self):
        """
        Test that a valid API key with write access is granted access.
        """
        request = self._make_request(self.valid_key)
        view = DummyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_key_without_write_access(self):
        """
        Test that an API key without write access is denied with a 403 response.
        """
        request = self._make_request(self.no_write_key)
        view = DummyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_expired_key(self):
        """
        Test that an expired API key is denied with a 403 response.
        """
        request = self._make_request(self.expired_key)
        view = DummyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_missing_key(self):
        """
        Test that a request without an API key is denied with a 403 response.
        """
        request = self.factory.get("/dummy-endpoint/")
        view = DummyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)
