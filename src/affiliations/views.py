"""Views for the affiliations service."""

# Third-party dependencies:
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from django.http import JsonResponse

# In-house code:
from affiliations.models import Affiliation, Approver
from affiliations.serializers import AffiliationSerializer


class AffiliationsList(generics.ListCreateAPIView):
    """List all affiliations, or create a new affiliation."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer


class AffiliationsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an affiliation."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer


@api_view(["GET"])
def affiliations_list_json_format(request):  # pylint: disable=unused-argument
    """List all affiliations in old JSON format."""
    affils_queryset = Affiliation.objects.filter(is_deleted=False).values()
    response_obj = {}
    for affil in affils_queryset:
        affil_type = affil["type"].lower()
        if affil["affiliation_id"] not in response_obj:
            old_json_format = {
                "affiliation_id": affil["affiliation_id"],
                "affiliation_fullname": affil["full_name"],
                "subgroups": {
                    affil_type: {
                        "id": affil["expert_panel_id"],
                        "fullname": affil["full_name"],
                    },
                },
                "approver": [],
            }
            response_obj[affil["affiliation_id"]] = old_json_format

        elif affil_type not in response_obj[affil["affiliation_id"]]["subgroups"]:
            response_obj[affil["affiliation_id"]]["affiliation_fullname"] = (
                response_obj[affil["affiliation_id"]]["affiliation_fullname"]
                + "/"
                + affil["type"]
            )
            response_obj[affil["affiliation_id"]]["subgroups"][affil_type] = {
                affil_type: {
                    "id": affil["expert_panel_id"],
                    "fullname": affil["full_name"],
                },
            }
        approvers_queryset = Approver.objects.filter(
            affiliation_id=affil["id"]
        ).values_list("approver_name", flat=True)
        for name in approvers_queryset:
            response_obj[affil["affiliation_id"]]["approver"].append(name)

    return JsonResponse(list(response_obj.values()), status=200, safe=False)


@api_view(["GET"])
def affiliation_detail_json_format(request):
    """List specific affiliation in old JSON format."""
    affil_id = request.GET.get("affil_id")
    affils_queryset = Affiliation.objects.filter(
        affiliation_id=affil_id, is_deleted=False
    ).values()
    response_obj = {}
    for affil in affils_queryset:
        affil_type = affil["type"].lower()
        if affil["affiliation_id"] not in response_obj:
            old_json_format = {
                "affiliation_id": affil["affiliation_id"],
                "affiliation_fullname": affil["full_name"],
                "subgroups": {
                    affil_type: {
                        "id": affil["expert_panel_id"],
                        "fullname": affil["full_name"],
                    },
                },
                "approver": [],
            }
            response_obj[affil["affiliation_id"]] = old_json_format

        elif affil_type not in response_obj[affil["affiliation_id"]]["subgroups"]:
            response_obj[affil["affiliation_id"]]["affiliation_fullname"] = (
                response_obj[affil["affiliation_id"]]["affiliation_fullname"]
                + "/"
                + affil["full_name"]
            )
            response_obj[affil["affiliation_id"]]["subgroups"][affil_type] = {
                affil_type: {
                    "id": affil["expert_panel_id"],
                    "fullname": affil["full_name"],
                },
            }
        approvers_queryset = Approver.objects.filter(
            affiliation_id=affil["id"]
        ).values_list("approver_name", flat=True)
        for name in approvers_queryset:
            response_obj[affil["affiliation_id"]]["approver"].append(name)

    return JsonResponse(list(response_obj.values()), status=200, safe=False)
