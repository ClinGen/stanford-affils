"""URLs for the affiliations service."""

# Third-party dependencies:
from django.urls import path
from django.urls import URLResolver, URLPattern
from rest_framework.urlpatterns import format_suffix_patterns

# In-house code:
from affiliations import views

urlpatterns: list[URLResolver | URLPattern] = [
    path("", views.AffiliationsList.as_view()),
    path("<int:pk>/", views.AffiliationsDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
