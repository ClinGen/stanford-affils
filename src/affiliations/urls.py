"""URLs for the affiliations service."""

# Third-party dependencies:
from django.urls import path
from django.urls import URLResolver, URLPattern
from rest_framework.urlpatterns import format_suffix_patterns

# In-house code:
from affiliations import views

urlpatterns: list[URLResolver | URLPattern] = [
    path("database_list/", views.AffiliationsList.as_view()),
    path("database_list/<int:pk>/", views.AffiliationsDetail.as_view()),
    path(
        "affiliations_list/",
        views.affiliations_list_json_format,
    ),
    path(
        "affiliation_detail/",
        views.affiliation_detail_json_format,
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
