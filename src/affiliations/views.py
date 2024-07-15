"""Views for the affiliations service."""

# Third-party dependencies:
from rest_framework import generics
from rest_framework import permissions

# In-house code:
from affiliations.models import Affiliation
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
