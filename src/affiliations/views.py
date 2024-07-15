"""Views for the affiliations service."""

# Third-party dependencies:
from rest_framework import generics

# In-house code:
from affiliations.models import Affiliation
from affiliations.serializers import AffiliationSerializer


class AffiliationsList(generics.ListCreateAPIView):
    """List all affiliations, or create a new affiliation."""

    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer


class AffiliationsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an affiliation."""

    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
