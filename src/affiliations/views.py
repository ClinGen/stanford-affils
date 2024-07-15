"""Views for the affiliations service."""

# Third-party dependencies:
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

# In-house code:
from affiliations.models import Affiliation
from affiliations.serializers import AffiliationSerializer


@csrf_exempt
def affiliations_list(request):  # pylint: disable=inconsistent-return-statements
    """List all affiliations, or create a new affiliation."""
    if request.method == "GET":
        affiliations = Affiliation.objects.all()
        serializer = AffiliationSerializer(affiliations, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = AffiliationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def affiliations_detail(  # pylint: disable=inconsistent-return-statements
    request, affiliation_id
):
    """Retrieve, update or delete an affiliation."""
    try:
        affiliation = Affiliation.objects.get(affiliation_id=affiliation_id)
    except Affiliation.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = AffiliationSerializer(affiliation)
        return JsonResponse(serializer.data)

    if request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = AffiliationSerializer(affiliation, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    if request.method == "DELETE":
        affiliation.delete()
        return HttpResponse(status=204)
