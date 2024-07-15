"""Views for the affiliations service."""

# pylint: disable=redefined-builtin
# pylint: disable=unused-argument

# Third-party dependencies:
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# In-house code:
from affiliations.models import Affiliation
from affiliations.serializers import AffiliationSerializer


@api_view(["GET", "POST"])
def affiliations_list(  # pylint: disable=inconsistent-return-statements
    request, format=None
):
    """List all affiliations, or create a new affiliation."""
    if request.method == "GET":
        affiliations = Affiliation.objects.all()
        serializer = AffiliationSerializer(affiliations, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = AffiliationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def affiliations_detail(  # pylint: disable=inconsistent-return-statements
    request, affiliation_id, format=None
):
    """Retrieve, update or delete an affiliation."""
    try:
        affiliation = Affiliation.objects.get(affiliation_id=affiliation_id)
    except Affiliation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AffiliationSerializer(affiliation)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = AffiliationSerializer(affiliation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        affiliation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
