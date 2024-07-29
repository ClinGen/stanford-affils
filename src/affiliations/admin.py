"""Admin config for the affiliations service."""

# Third-party dependencies:
from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin  # type: ignore
from affiliations.models import Affiliation, Coordinator, Approver


class AffiliationForm(forms.ModelForm):
    """Create forms to display information in Admin page."""

    class Meta:
        """Meta class for forms"""

        fields = "__all__"
        model = Affiliation
        widgets = {
            "status": forms.Select(
                choices=[
                    ("Active", "Active"),
                    ("Applying", "Applying"),
                    ("Inactive", "Inactive"),
                    ("Retired", "Retired"),
                ]
            ),
            "type": forms.Select(
                choices=[
                    ("Variant Curation Expert Panel", "Variant Curation Expert Panel"),
                    ("Gene Curation Expert Panel", "Gene Curation Expert Panel"),
                    ("Independent Curation Group", "Independent Curation Group"),
                ]
            ),
            "clinical_domain_working_group": forms.Select(
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


class CoordinatorInlineAdmin(admin.TabularInline):
    """Configure the coordinators admin panel."""

    model = Coordinator
    extra = 1


class ApproverInlineAdmin(admin.TabularInline):
    """Configure the approvers admin panel."""

    model = Approver
    extra = 1


class AffiliationsAdmin(ModelAdmin):
    """Configure the affiliations admin panel."""

    form = AffiliationForm
    search_fields = ["affiliation_id", "full_name", "abbreviated_name"]
    # pylint:disable=duplicate-code
    list_display = [
        "affiliation_id",
        "full_name",
        "abbreviated_name",
        "status",
        "type",
        "clinical_domain_working_group",
    ]

    inlines = [CoordinatorInlineAdmin, ApproverInlineAdmin]


    def get_readonly_fields(self, request, obj=None):
        """ID is editable upon creation, afterwards, it is read only"""
        # pylint:disable=unused-argument
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
