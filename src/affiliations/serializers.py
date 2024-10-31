"""Serializers and deserializers for the affiliations service."""

# Third-party dependencies:
from rest_framework import serializers

# In-house code:
from affiliations.models import Affiliation, Coordinator, Approver, Submitter


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


class SubmitterSerializer(serializers.ModelSerializer):
    """Serialize Clinvar Submitter ID objects."""

    class Meta:
        """Describe the fields on an Submitter ID object."""

        model = Submitter
        fields = [
            "clinvar_submitter_id",
        ]


class AffiliationSerializer(serializers.ModelSerializer):
    """Serialize Affiliation objects."""

    coordinators = CoordinatorSerializer(many=True)
    approvers = ApproverSerializer(many=True)
    clinvar_submitter_ids = SubmitterSerializer(many=True)

    class Meta:
        """Describe the fields on an Affiliation object."""

        model = Affiliation
        fields = [
            "affiliation_id",
            "expert_panel_id",
            "full_name",
            "short_name",
            "status",
            "type",
            "clinical_domain_working_group",
            "members",
            "approvers",
            "coordinators",
            "clinvar_submitter_ids",
            "is_deleted",
        ]

    def create(self, validated_data):
        """Create and return an Affiliations instance."""
        coordinators_data = validated_data.pop("coordinators")
        approvers_data = validated_data.pop("approvers")
        submitter_ids_data = validated_data.pop("clinvar_submitter_ids")

        affil = Affiliation.objects.create(
            **validated_data
        )  # pylint: disable=no-member
        for coordinator_data in coordinators_data:
            Coordinator.objects.create(affilation=affil, **coordinator_data)
        for approver_data in approvers_data:
            Approver.objects.create(affilation=affil, **approver_data)
        for submitter_id_data in submitter_ids_data:
            Submitter.objects.create(affilation=affil, **submitter_id_data)
        return affil

    def update(self, instance, validated_data):
        """Update and return an existing Affiliations instance."""
        coordinator_data = validated_data.pop("coordinators")
        coordinators = instance.coordinators

        approver_data = validated_data.pop("approvers")
        approvers = instance.approvers

        submitter_id_data = validated_data.pop("clinvar_submitter_ids")
        clinvar_submitter_ids = instance.clinvar_submitter_ids

        instance.affiliation_id = validated_data.IntegerField()
        instance.expert_panel_id = validated_data.IntegerField()
        instance.full_name = validated_data.CharField()
        instance.short_name = validated_data.CharField()
        instance.status = validated_data.CharField()
        instance.type = validated_data.CharField()
        instance.clinical_domain_working_group = validated_data.CharField()
        instance.members = validated_data.CharField()
        instance.is_deleted = validated_data.BooleanField()

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

        clinvar_submitter_ids.clinvar_submitter_id = submitter_id_data.get(
            "clinvar_submitter_id", clinvar_submitter_ids.clinvar_submitter_id
        )
        clinvar_submitter_ids.save()

        return instance
