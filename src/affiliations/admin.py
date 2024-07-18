"""Admin config for the affiliations service."""

# Third-party dependencies:
from django.contrib import admin

# In-house code:
from affiliations.models import Affiliation


class AffiliationsAdmin(admin.ModelAdmin):
    """Configure the affiliations admin panel."""

    search_fields = ["affiliation_id", "name"]


# Add models we want to be able to edit in the admin interface.
admin.site.register(Affiliation, AffiliationsAdmin)

# Change the admin site's display name.
admin.site.site_header = "Affiliations Service Admin Panel"
