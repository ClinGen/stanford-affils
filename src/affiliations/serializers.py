"""Serializers and deserializers for the affiliations service."""

# Third-party dependencies:
from rest_framework import serializers

# In-house code:
from affiliations.models import Affiliation, Coordinator, Approver


class CoordinatorSerializer(serializers.ModelSerializer):
    """Serialize Coordinator objects."""

    class Meta:
        """Describe the fields on an Coordinator object."""

        model = Coordinator
        fields = [
            "coordinator_name",
            "coordinator_email",
        ]


class ApproverSerializer(serializers.ModelSerializer):
    """Serialize Approver objects."""

    class Meta:
        """Describe the fields on an Approver object."""

        model = Approver
        fields = [
            "approver_name",
        ]


class AffiliationSerializer(serializers.ModelSerializer):
    """Serialize Affiliation objects."""

    coordinators = CoordinatorSerializer(many=True)
    approvers = ApproverSerializer(many=True)

    class Meta:
        """Describe the fields on an Affiliation object."""

        model = Affiliation
        fields = [
            "affiliation_id",
            "full_name",
            "abbreviated_name",
            "status",
            "type",
            "clinical_domain_working_group",
            "members",
            "clinvar_submitter_ids",
            "approvers",
            "coordinators",
        ]

    def create(self, validated_data):
        """Create and return an Affiliations instance."""
        coordinators_data = validated_data.pop("coordinators")
        approvers_data = validated_data.pop("approvers")

        affil = Affiliation.objects.create(
            **validated_data
        )  # pylint: disable=no-member
        for coordinator_data in coordinators_data:
            Coordinator.objects.create(affilation=affil, **coordinator_data)
        for approver_data in approvers_data:
            Approver.objects.create(affilation=affil, **approver_data)
        return affil

    def update(self, instance, validated_data):
        """Update and return an existing Affiliations instance."""
        coordinator_data = validated_data.pop("coordinators")
        coordinators = instance.coordinators

        approver_data = validated_data.pop("approvers")
        approvers = instance.approvers

        instance.affiliation_id = validated_data.IntegerField()
        instance.full_name = validated_data.CharField()
        instance.abbreviated_name = validated_data.CharField()
        instance.status = validated_data.CharField()
        instance.type = validated_data.CharField()
        instance.clinical_domain_working_group = validated_data.CharField()
        instance.members = validated_data.CharField()
        instance.clinvar_submitter_ids = validated_data.CharField()
        instance.save()

        coordinators.coordinator_name = coordinator_data.get(
            "coordinator_name", coordinators.coordinator_name
        )
        coordinators.coordinator_email = coordinator_data.get(
            "coordinator_email", coordinators.coordinator_email
        )
        coordinators.save()

        approvers.approver_name = approver_data.get(
            "approver_name", approvers.approver_name
        )
        approvers.save()

        return instance
