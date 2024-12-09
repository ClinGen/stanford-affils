"""Views for the affiliations service."""

# Third-party dependencies:
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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


@login_required
@api_view(["GET"])
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
            response_obj[affil_id]["approver"].append(name)

    return JsonResponse(
        list(response_obj.values()),
        status=200,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


@login_required
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
            response_obj[affil_id]["approver"].append(name)
    return JsonResponse(
        list(response_obj.values()),
        status=200,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )
