"""Admin config for the affiliations service."""

# Third-party dependencies:
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

from unfold.forms import (  # type: ignore
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from unfold.admin import (  # type: ignore
    ModelAdmin,
    TabularInline,
    UnfoldAdminSelectWidget,
)

# In-house code:
from affiliations.models import (
    Affiliation,
    Coordinator,
    Approver,
    Submitter,
)

# Unregistering base Django Admin User and Group to use Unfold User and Group
# instead for styling purposes.
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """Register Unfold user admin for styling of Users page."""

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Register Unfold group admin for styling of Group page."""


class AffiliationForm(forms.ModelForm):
    """Create forms to display information in Admin page."""

    class Meta:
        """Meta class for forms"""

        fields = "__all__"
        model = Affiliation
        widgets = {
            "status": UnfoldAdminSelectWidget(
                choices=[
                    ("Active", "Active"),
                    ("Applying", "Applying"),
                    ("Inactive", "Inactive"),
                    ("Retired", "Retired"),
                ]
            ),
            "type": UnfoldAdminSelectWidget(
                choices=[
                    ("Variant Curation Expert Panel", "Variant Curation Expert Panel"),
                    ("Gene Curation Expert Panel", "Gene Curation Expert Panel"),
                    ("Independent Curation Group", "Independent Curation Group"),
                ]
            ),
            "clinical_domain_working_group": UnfoldAdminSelectWidget(
                choices=[
                    ("None", "None"),
                    ("Cardiovascular", "Cardiovascular"),
                    ("Hearing Loss", "Hearing Loss"),
                    ("Hemostasis/Thrombosis", "Hemostasis/Thrombosis"),
                    ("Hereditary Cancer", "Hereditary Cancer"),
                    ("Immunology", "Immunology"),
                    ("Inborn Errors of Metabolism", "Inborn Errors of Metabolism"),
                    ("Kidney Disease", "Kidney Disease"),
                    ("Neurodevelopmental Disorders", "Neurodevelopmental Disorders"),
                    ("Neurological Disorders", "Neurological Disorders"),
                    ("Ocular", "Ocular"),
                    ("Other", "Other"),
                    ("Pulmonary", "Pulmonary"),
                    ("RASopathy", "RASopathy"),
                    (
                        "Rheumatologic Autoimmune Disease",
                        "Rheumatologic Autoimmune Disease",
                    ),
                    ("Skeletal Disorders", "Skeletal Disorders"),
                    ("Somatic Cancer", "Somatic Cancer"),
                ]
            ),
        }


class CoordinatorInlineAdmin(TabularInline):
    """Configure the coordinators admin panel."""

    model = Coordinator
    extra = 1

class ApproverInlineAdmin(TabularInline):
    """Configure the approvers admin panel."""

    model = Approver
    extra = 1

class SubmitterInlineAdmin(TabularInline):
    """Configure the clinvar submitter IDs admin panel."""

    model = Submitter
    extra = 1


class AffiliationsAdmin(ModelAdmin):
    """Configure the affiliations admin panel."""

    form = AffiliationForm
    search_fields = [
        "affiliation_id",
        "curation_panel_id",
        "full_name",
        "abbreviated_name",
    ]
    # pylint:disable=duplicate-code
    list_display = [
        "affiliation_id",
        "curation_panel_id",
        "full_name",
        "abbreviated_name",
        "status",
        "type",
        "clinical_domain_working_group",
    ]

    # pylint:disable=duplicate-code
    list_display_links = [
        "affiliation_id",
        "curation_panel_id",
        "full_name",
        "abbreviated_name",
        "status",
        "type",
        "clinical_domain_working_group",
    ]
    inlines = [CoordinatorInlineAdmin, ApproverInlineAdmin, SubmitterInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        """ID is editable upon creation, afterwards, it is read only"""
        # pylint:disable=unused-argument
        if obj is None:
            return [
                "members",
            ]
        return [
            "affiliation_id",
            "curation_panel_id",
            "members",
        ]


# Add models we want to be able to edit in the admin interface.
admin.site.register(Affiliation, AffiliationsAdmin)

# Change the admin site's display name.
admin.site.site_title = "Affils Service"
admin.site.site_header = "Affiliation Service Panel"
admin.site.index_title = "Welcome to the ClinGen Affiliation Service Portal"
