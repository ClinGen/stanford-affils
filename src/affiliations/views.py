"""Views for the affiliations service."""

# Third-party dependencies:
import logging
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_api_key.permissions import HasAPIKey
from django.http import JsonResponse

# In-house code:
from affiliations.models import Affiliation, Approver, ClinicalDomainWorkingGroup
from affiliations.serializers import AffiliationSerializer, ClinicalDomainWorkingGroupSerializer


def custom_exception_handler(exc, context):
    """Add custom consistent error responses."""
    response = exception_handler(exc, context)
    if response is not None:
        return Response(
            {
                "error": "Request Failed",
                "details": response.data,
            },
            status=response.status_code,
        )
    logging.error("Unhandled exception", exc_info=exc)

    return Response(
        {
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred.",
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


class AffiliationsList(generics.ListCreateAPIView):
    """List all affiliations, or create a new affiliation."""

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer


class AffiliationsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an affiliation."""

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer


class AffiliationUpdateView(generics.RetrieveUpdateAPIView):
    """Update editable affiliation data, return all affiliation information."""

    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
    lookup_field = "affiliation_id"

class CDWGListView(generics.ListAPIView):
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = ClinicalDomainWorkingGroup.objects.all()
    serializer_class = ClinicalDomainWorkingGroupSerializer


@api_view(["GET"])
@permission_classes([HasAPIKey | IsAuthenticated])
def affiliations_list_json_format(request):  # pylint: disable=unused-argument
    """List all affiliations in old JSON format."""
    affils_queryset = Affiliation.objects.filter(is_deleted=False).values()
    response_obj = {}
    for affil in affils_queryset:
        affil_type = affil["type"].lower()
        # In old JSON, SC-VCEPS are only considered VCEPS.
        if affil_type == "sc_vcep":
            affil_type = "vcep"
        # In old JSON, Affiliation IDs and EP Ids are in string format.
        affil_id = str(affil["affiliation_id"])
        ep_id = str(affil["expert_panel_id"])

        if affil_id not in response_obj:
            if affil_type in ["vcep", "gcep"]:
                old_json_format = {
                    "affiliation_id": affil_id,
                    "affiliation_fullname": affil["full_name"],
                    "subgroups": {
                        affil_type: {
                            "id": ep_id,
                            "fullname": affil["full_name"],
                        },
                    },
                }
            # Independent curation group format
            else:
                old_json_format = {
                    "affiliation_id": affil_id,
                    "affiliation_fullname": affil["full_name"],
                }
            response_obj[affil_id] = old_json_format
        elif affil_type not in response_obj[affil_id]["subgroups"]:
            # If VCEP or GCEP in full name, add other subgroup to end of name.
            if ("VCEP" in response_obj[affil_id]["affiliation_fullname"]) or (
                "GCEP" in response_obj[affil_id]["affiliation_fullname"]
            ):
                response_obj[affil_id]["affiliation_fullname"] = (
                    response_obj[affil_id]["affiliation_fullname"] + "/" + affil["type"]
                )
            # Else append affiliation subgroup name to full name
            else:
                response_obj[affil_id]["affiliation_fullname"] = (
                    response_obj[affil_id]["affiliation_fullname"]
                    + "/"
                    + affil["full_name"]
                )

            response_obj[affil_id]["subgroups"][affil_type] = {
                "id": ep_id,
                "fullname": affil["full_name"],
            }
        # If there are approvers, add them to the object.
        approvers_queryset = Approver.objects.filter(
            affiliation_id=affil["id"]
        ).values_list("approver_name", flat=True)
        if approvers_queryset and "approver" not in response_obj[affil_id]:
            response_obj[affil_id]["approver"] = []
        for name in approvers_queryset:
            if name not in response_obj[affil_id]["approver"]:
                response_obj[affil_id]["approver"].append(name)

    return JsonResponse(
        list(response_obj.values()),
        status=200,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


@api_view(["GET"])
@permission_classes([HasAPIKey | IsAuthenticated])
def affiliation_detail_json_format(request):
    """List specific affiliation in old JSON format."""
    affil_id = request.GET.get("affil_id")
    affils_queryset = Affiliation.objects.filter(
        affiliation_id=affil_id, is_deleted=False
    ).values()
    response_obj = {}
    for affil in affils_queryset:
        affil_type = affil["type"].lower()
        # In old JSON, SC-VCEPS are only considered VCEPS.
        if affil_type == "sc_vcep":
            affil_type = "vcep"
        # In old JSON, Affiliation IDs and EP Ids are in string format.
        affil_id = str(affil["affiliation_id"])
        ep_id = str(affil["expert_panel_id"])

        if affil_id not in response_obj:
            if affil_type in ["vcep", "gcep"]:
                old_json_format = {
                    "affiliation_id": affil_id,
                    "affiliation_fullname": affil["full_name"],
                    "subgroups": {
                        affil_type: {
                            "id": ep_id,
                            "fullname": affil["full_name"],
                        },
                    },
                }
            # Independent curation group format
            else:
                old_json_format = {
                    "affiliation_id": affil_id,
                    "affiliation_fullname": affil["full_name"],
                }
            response_obj[affil_id] = old_json_format
        elif affil_type not in response_obj[affil_id]["subgroups"]:
            # If VCEP or GCEP in full name, add other subgroup to end of name.
            if ("VCEP" in response_obj[affil_id]["affiliation_fullname"]) or (
                "GCEP" in response_obj[affil_id]["affiliation_fullname"]
            ):
                response_obj[affil_id]["affiliation_fullname"] = (
                    response_obj[affil_id]["affiliation_fullname"] + "/" + affil["type"]
                )
            # Else append affiliation subgroup name to full name
            else:
                response_obj[affil_id]["affiliation_fullname"] = (
                    response_obj[affil_id]["affiliation_fullname"]
                    + "/"
                    + affil["full_name"]
                )

            response_obj[affil_id]["subgroups"][affil_type] = {
                "id": ep_id,
                "fullname": affil["full_name"],
            }
        # If there are approvers, add them to the object.
        approvers_queryset = Approver.objects.filter(
            affiliation_id=affil["id"]
        ).values_list("approver_name", flat=True)
        if approvers_queryset and "approver" not in response_obj[affil_id]:
            response_obj[affil_id]["approver"] = []
        for name in approvers_queryset:
            if name not in response_obj[affil_id]["approver"]:
                response_obj[affil_id]["approver"].append(name)
    return JsonResponse(
        list(response_obj.values()),
        status=200,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


@api_view(["POST"])
@permission_classes([HasAPIKey | IsAuthenticated])
def create_affiliation(request):
    """Handle POST request to create a new affiliation, return affiliation_id
    and expert_panel_id in response."""
    serializer = AffiliationSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response(
            {
                "affiliation_id": instance.affiliation_id,
                "expert_panel_id": instance.expert_panel_id,
            },
            status=status.HTTP_201_CREATED,
        )
    logging.warning("Affiliation creation failed: %s", serializer.errors)
    return Response(
        {
            "error": "Validation Failed",
            "details": serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )
