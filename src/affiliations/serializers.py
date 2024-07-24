"""Serializers and deserializers for the affiliations service."""

# Third-party dependencies:
from rest_framework import serializers

# In-house code:
from affiliations.models import Affiliation


class AffiliationSerializer(serializers.ModelSerializer):
    """Serialize Affiliation objects."""

    class Meta:
        """Describe the fields on an Affiliation object."""

        model = Affiliation
        fields = [
            "affiliation_id",
            "full_name",
            "abbreviated_name",
            "coordinator",
            "coordinator_email",
            "status",
            "type",
            "clinical_domain_working_group",
            "members",
            "approvers",
            "clinvar_submitter_ids",
        ]

    def create(self, validated_data):
        """Create and return an Affiliations instance."""
        return Affiliation.objects.create(**validated_data)  # pylint: disable=no-member

    def update(self, instance, validated_data):
        """Update and return an existing Affiliations instance."""
        instance.affiliation_id = validated_data.IntegerField()
        instance.full_name = validated_data.CharField()
        instance.abbreviated_name = validated_data.CharField()
        instance.coordinator = validated_data.CharField()
        instance.coordinator_email = validated_data.EmailField()
        instance.status = validated_data.CharField()
        instance.type = validated_data.CharField()
        instance.clinical_domain_working_group = validated_data.CharField()
        instance.members = validated_data.CharField()
        instance.approvers = validated_data.CharField()
        instance.clinvar_submitter_ids = validated_data.CharField()
        instance.save()
        return instance
