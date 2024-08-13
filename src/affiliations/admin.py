"""Admin config for the affiliations service."""

# Third-party dependencies:
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.core.exceptions import ValidationError

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

    class Media:
        """Media styling for selector widget on User page"""

        css = {"all": ("css/permissions.css",)}


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Register Unfold group admin for styling of Group page."""

    class Media:
        """Media styling for selector widget on Group page"""

        css = {"all": ("css/permissions.css",)}


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

    def clean(self):
        cleaned_data = super().clean()
        affil_id = cleaned_data.get("affiliation_id")
        ep_id = cleaned_data.get("expert_panel_id")
        _type = cleaned_data.get("type")
        full_name = cleaned_data.get("full_name")

        if affil_id is None or full_name is None:
            # Allow Django to handle require field validation error.
            pass
        if self.instance.pk is not None:
            return
        if Affiliation.objects.filter(
            affiliation_id=affil_id, expert_panel_id=ep_id
        ).exists():
            self.add_error(
                None,
                ValidationError(
                    "This Affiliation ID and Expert Panel ID pair already exist."
                ),
            )
        if (
            _type == "Independent Curation Group"
            and self.cleaned_data["expert_panel_id"] is not None
        ):
            self.add_error(
                "expert_panel_id",
                ValidationError(
                    "If type Independent Curation Group is selected, "
                    "Expert Panel ID must be left blank."
                ),
            )
            if affil_id < 10000 or affil_id >= 20000:
                self.add_error(
                    "affiliation_id",
                    ValidationError(
                        "Valid Affiliation ID's should be in the 10000 number range. "
                        "Please include a valid Affiliation ID."
                    ),
                )
        if _type == "Gene Curation Expert Panel":
            if ep_id is None or (ep_id < 40000 or ep_id >= 50000):
                self.add_error(
                    "expert_panel_id",
                    ValidationError(
                        "Valid GCEP ID's should be in the 40000 number range. "
                        "Please include a valid Expert Panel ID."
                    ),
                )
            if affil_id - 10000 != ep_id - 40000:
                self.add_error(
                    None,
                    ValidationError(
                        "The Affiliation ID and Expert Panel ID do not match."
                    ),
                )
        if _type == "Variant Curation Expert Panel":
            if ep_id is None or (ep_id < 50000 or ep_id >= 60000):
                self.add_error(
                    "expert_panel_id",
                    ValidationError(
                        "Valid VCEP ID's should be in the  50000 number range. "
                        "Please include a valid Expert Panel ID."
                    ),
                )
            if affil_id - 10000 != ep_id - 50000:
                self.add_error(
                    None,
                    ValidationError(
                        "The Affiliation ID and Expert Panel ID do not match."
                    ),
                )


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
        "expert_panel_id",
        "full_name",
        "abbreviated_name",
    ]
    # pylint:disable=duplicate-code
    list_display = [
        "affiliation_id",
        "expert_panel_id",
        "full_name",
        "abbreviated_name",
        "status",
        "type",
        "clinical_domain_working_group",
    ]

    # pylint:disable=duplicate-code
    list_display_links = [
        "affiliation_id",
        "expert_panel_id",
        "full_name",
        "abbreviated_name",
        "status",
        "type",
        "clinical_domain_working_group",
    ]
    inlines = [CoordinatorInlineAdmin, ApproverInlineAdmin, SubmitterInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        """Fields that are editable upon creation, afterwards, are read only"""
        # pylint:disable=unused-argument
        if obj is None:
            return [
                "members",
            ]
        return [
            "affiliation_id",
            "expert_panel_id",
            "type",
            "clinical_domain_working_group",
            "members",
        ]


# Add models we want to be able to edit in the admin interface.
admin.site.register(Affiliation, AffiliationsAdmin)

# Change the admin site's display name.
admin.site.site_title = "Affils Service"
admin.site.site_header = "Affiliation Service Panel"
admin.site.index_title = "Welcome to the ClinGen Affiliation Service Portal"
