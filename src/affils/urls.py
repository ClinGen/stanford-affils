"""URLs for the the affiliations service."""

# Third-party dependencies:
from django.urls import path

# In-house code:
from affils import views

urlpatterns = [
    path("", views.affiliations_list),
    path("<int:affiliation_id>/", views.affiliations_detail),
]
