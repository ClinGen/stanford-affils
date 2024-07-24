"""Admin config for the affiliations service."""

# Third-party dependencies:
from django.contrib import admin
from unfold.admin import ModelAdmin

# In-house code:
from affiliations.models import Affiliation


class AffiliationsAdmin(ModelAdmin):
    """Configure the affiliations admin panel."""

    search_fields = ["affiliation_id", "full_name", "abbreviated_name"]
    list_display = [
        "affiliation_id",
        "full_name",
        "abbreviated_name",
        "status",
        "type",
        "clinical_domain_working_group",
    ]

    def get_readonly_fields(self, obj=None):
        """ID is editable upon creation, afterwards, it is read only"""
        if obj is None:
            return [
                "members",
            ]
        return [
            "affiliation_id",
            "members",
        ]


# Add models we want to be able to edit in the admin interface.
admin.site.register(Affiliation, AffiliationsAdmin)

# Change the admin site's display name.
admin.site.site_header = "Affiliations Service Admin Panel"
