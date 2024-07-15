"""URLs for the affiliations service."""

# Third-party dependencies:
from django.urls import path

# In-house code:
from affiliations import views

urlpatterns = [
    path("", views.affiliations_list),
    path("<int:affiliation_id>/", views.affiliations_detail),
]
