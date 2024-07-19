"""Admin config for the affiliations service."""

# Third-party dependencies:
from django.contrib import admin

# In-house code:
from affiliations.models import Affiliation, Coordinator


class CoordinatorInline(admin.TabularInline):
    """Configure the coordinators admin panel"""
    model = Coordinator
    extra = 0


class AffiliationsAdmin(admin.ModelAdmin):
    """Configure the affiliations admin panel."""
    search_fields = ["affiliation_id", "name"]
    list_display = ["affiliation_id", "name", "status", "type", "family"]
    fields = ("affiliation_id", "name", "status", "type", "family",
              "approvers", "clinvar_submitter_ids", "members")
    inlines = [CoordinatorInline]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ["members",]
        return ["affiliation_id", "members",]


# Add models we want to be able to edit in the admin interface.
admin.site.register(Affiliation, AffiliationsAdmin)

# Change the admin site's display name.
admin.site.site_header = "Affiliations Service Admin Panel"
