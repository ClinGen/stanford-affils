"""Tests for the affiliations service."""

# Third-party dependencies:
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from rest_framework_api_key.models import APIKey

# In-house code:
from affiliations.models import (
    Affiliation,
    Coordinator,
    Approver,
    Submitter,
    ClinicalDomainWorkingGroup,
)

from affiliations.serializers import AffiliationSerializer
from affiliations.utils import (
    generate_next_affiliation_id,
    validate_and_set_expert_panel_id,
)


class AffiliationsViewsBaseTestCase(APITestCase):
    """A base test class with setup for testing affiliations views."""

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        """Seed the test database with some test data."""
        _, cls.api_key = APIKey.objects.create_key(name="test-service")
        cls.auth_headers = {"HTTP_X_API_KEY": cls.api_key}
        cdwg1, _ = ClinicalDomainWorkingGroup.objects.get_or_create(
            code="HEARING_LOSS", defaults={"name": "Hearing Loss"}
        )
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
        validate_and_set_expert_panel_id(cls.success_affiliation)
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
        response = self.client.get(
            "/api/affiliation_detail/?affil_id=10000", **self.auth_headers
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
        response = self.client.get("/api/affiliations_list/", **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_affiliation__success(self):
        """Test successful creation of affiliation via POST API with valid data."""
        response = self.client.post(
            "/api/affiliation/create/",
            self.create_data,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("affiliation_id", response.data)
        self.assertIn("expert_panel_id", response.data)

    def test_create_affiliation_missing_required_fields(self):
        """Test that missing required fields in POST request returns 400 and error messages."""
        response = self.client.post(
            "/api/affiliation/create/", {}, format="json", **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("full_name", response.data["details"])
        self.assertIn("type", response.data["details"])


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

    def test_validate_and_set_expert_panel_id_success(self):
        """Test that a valid SC_VCEP affiliation sets the correct expert_panel_id."""
        cleaned_data = {
            "affiliation_id": 10000,
            "type": "SC_VCEP",
            "clinical_domain_working_group": self.cdwg,
        }
        validate_and_set_expert_panel_id(cleaned_data)
        self.assertIn("expert_panel_id", cleaned_data)
        self.assertGreaterEqual(cleaned_data["expert_panel_id"], 50000)

    def test_validate_and_set_expert_panel_id_invalid_cdwg(self):
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
            validate_and_set_expert_panel_id(cleaned_data)
        self.assertIn(
            "If type is 'Somatic Cancer Variant Curation Expert Panel",
            str(context.exception),
        )

    def test_generate_next_affiliation_id_raises_value_error(self):
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
            validate_and_set_expert_panel_id(cleaned_data)

        self.assertIn("affiliation_id is required", str(cm.exception))


class TestAffiliationUpdateView(APITestCase):
    """Test cases for updating affiliations via API"""

    @classmethod
    def setUpTestData(cls):
        _, cls.api_key = APIKey.objects.create_key(name="test-service")
        cls.auth_headers = {"HTTP_X_API_KEY": cls.api_key}

        cls.cdwg = ClinicalDomainWorkingGroup.objects.create(name="Cardiology")
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
        payload = {
            "full_name": "Updated Name",
            "short_name": "UpdatedShort",
            "status": "INACTIVE",
        }
        response = self.client.patch(
            f"/api/affiliation/{self.affiliation.affiliation_id}/update/",
            data=payload,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.affiliation.refresh_from_db()
        self.assertEqual(self.affiliation.full_name, "Updated Name")
        self.assertEqual(self.affiliation.status, "INACTIVE")

    def test_update_affiliation_fails_on_immutable_field(self):
        """Test to attempt to update an immutable field via API."""
        payload = {"type": "VCEP"}
        response = self.client.patch(
            f"/api/affiliation/{self.affiliation.affiliation_id}/update/",
            data=payload,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data["details"])
