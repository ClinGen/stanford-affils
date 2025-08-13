"""Admin config for the affiliations service."""

# Third-party dependencies:
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.admin import APIKeyModelAdmin
from import_export.admin import ExportMixin  # type: ignore
from import_export import resources  # type: ignore


from unfold.contrib.import_export.forms import SelectableFieldsExportForm  # type: ignore
from unfold.forms import (  # type: ignore
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from unfold.admin import (  # type: ignore
    ModelAdmin,
    TabularInline,
)

from unfold.contrib.filters.admin import (  # type: ignore
    ChoicesDropdownFilter,
    MultipleChoicesDropdownFilter,
)

# In-house code:
from affiliations.models import (
    Affiliation,
    Coordinator,
    Approver,
    Submitter,
    ClinicalDomainWorkingGroup,
)

from affiliations.utils import (
    generate_next_affiliation_id,
    set_expert_panel_id,
    validate_unique_cdwg_name,
    validate_cdwg_matches_type,
)
from .models import CustomAPIKey

# Unregistering base Django Admin User and Group to use Unfold User and Group
# instead for styling purposes.
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(APIKey)


@admin.register(CustomAPIKey)
class CustomAPIKeyAdmin(APIKeyModelAdmin, ModelAdmin):
    """Register Custom API Key model"""

    # Controls what fields are listed in overview header.
    list_display = ("name", "prefix", "created", "can_write", "expiry_date", "revoked")
    # Which links are "clickable"
    list_display_links = (
        "name",
        "prefix",
        "created",
        "can_write",
        "expiry_date",
        "revoked",
    )
    # Display Order
    fields = ("name", "can_write", "revoked", "expiry_date")


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """Register Unfold user admin for styling of Users page."""

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    class Media:
        """Media styling for selector widget on User page"""

        css = {"all": ("css/permissions.css",)}

    def get_fieldsets(self, request, obj=None):
        """Restricts which fields users can view. Superusers are able to
        view everything and have the option to create other superusers.
        While non-superusers have the ability to manage other staff level users."""
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        else:
            perm_fields = ("is_active", "is_staff", "groups", "user_permissions")

        return [
            (None, {"fields": ("username", "password")}),
            (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
            (_("Permissions"), {"fields": perm_fields}),
            (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        ]


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Register Unfold group admin for styling of Group page."""

    class Media:
        """Media styling for selector widget on Group page"""

        css = {"all": ("css/permissions.css",)}


class CDWGAdminForm(forms.ModelForm):
    """Create CDWG forms to validate information on Admin page."""

    class Meta:
        """Meta class for CDWGAdminforms"""

        model = ClinicalDomainWorkingGroup
        fields = "__all__"

    def clean_name(self):
        """Check to validate if duplicate CDWG name upon creation or update."""
        name = self.cleaned_data["name"]
        instance_id = self.instance.pk if self.instance else None
        validate_unique_cdwg_name(name, instance_id)
        return name


@admin.register(ClinicalDomainWorkingGroup)
class ClinicalDomainWorkingGroupAdmin(ModelAdmin):
    """Register CDWGs in Admin page"""

    form = CDWGAdminForm
    list_display = ("name", "id")
    search_fields = ("name", "id")


class AffiliationForm(forms.ModelForm):
    """Create forms to display information in Admin page."""

    class Meta:
        """Meta class for forms"""

        fields = "__all__"
        model = Affiliation

    @transaction.atomic
    def clean(self):
        cleaned_data = super().clean()
        # If the primary key already exists, return cleaned_data.
        # Otherwise, run validations on new affiliations
        if self.instance.pk is None:
            generate_next_affiliation_id(cleaned_data)
            set_expert_panel_id(cleaned_data)

            if (
                Affiliation.objects.select_for_update()
                .filter(
                    affiliation_id=cleaned_data.get("affiliation_id"),
                    expert_panel_id=cleaned_data.get("expert_panel_id"),
                )
                .exists()
            ):
                raise ValidationError(
                    "An affiliation with this Affiliation ID and Expert Panel ID already exists."
                )

        # Always validate CDWG-type relationship
        validate_cdwg_matches_type(cleaned_data, self.instance)
        return cleaned_data


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


class AffiliationResource(resources.ModelResource):
    """Configure affiliation export page."""

    class Meta:
        """Meta class for Affiliation Resource"""

        model = Affiliation

        # pylint:disable=duplicate-code
        fields = [
            "affiliation_id",
            "expert_panel_id",
            "full_name",
            "short_name",
            "status",
            "type",
            "clinical_domain_working_group__name",
            "is_deleted",
        ]


class AffiliationsAdmin(ExportMixin, ModelAdmin):  # pylint: disable=too-many-ancestors
    """Configure the affiliations admin panel."""

    form = AffiliationForm
    export_form_class = SelectableFieldsExportForm
    resource_class = AffiliationResource

    # Returns all DB values in export
    def get_export_queryset(self, request):
        return Affiliation.objects.all()

    # Controls which fields are searchable via the search bar.
    search_fields = [
        "affiliation_id",
        "expert_panel_id",
        "full_name",
        "short_name",
        "coordinators__coordinator_name",
        "coordinators__coordinator_email",
    ]

    # Controls what fields are listed in overview header.
    # pylint:disable=duplicate-code
    list_display = [
        "affiliation_id",
        "expert_panel_id",
        "full_name",
        "short_name",
        "status",
        "type",
        "clinical_domain_working_group",
        "get_coordinator_names",
        "get_coordinator_emails",
    ]

    # Controls what columns are "clickable" to enter detailed view.
    # pylint:disable=duplicate-code
    list_display_links = [
        "affiliation_id",
        "expert_panel_id",
        "full_name",
        "short_name",
        "status",
        "type",
        "clinical_domain_working_group",
        "get_coordinator_names",
        "get_coordinator_emails",
    ]

    @transaction.atomic
    def get_queryset(self, request):
        """Query to only display affiliations that have not been "soft-deleted"."""
        affiliations_query = super().get_queryset(request)
        return affiliations_query.filter(is_deleted=False)

    @admin.display(
        description="Coordinator Name", ordering="coordinators__coordinator_name"
    )
    def get_coordinator_names(self, obj):
        """Query coordinator names and return list of names"""
        coordinators = Coordinator.objects.filter(affiliation_id=obj.pk).values_list(
            "coordinator_name", flat=True
        )
        coordinator_names = []
        for name in coordinators:
            coordinator_names.append(name)
        return coordinator_names

    @admin.display(
        description="Coordinator Email",
    )
    def get_coordinator_emails(self, obj):
        """Query coordinator emails and return list of emails"""
        coordinators = Coordinator.objects.filter(affiliation_id=obj.pk).values_list(
            "coordinator_email", flat=True
        )
        coordinator_emails = []
        for email in coordinators:
            coordinator_emails.append(email)
        return coordinator_emails

    # Controls what fields can be filtered on.
    list_filter = [
        ("status", MultipleChoicesDropdownFilter),
        ("type", ChoicesDropdownFilter),
        ("clinical_domain_working_group", ChoicesDropdownFilter),
    ]
    list_filter_submit = True  # Submit button at the bottom of filter tab.
    list_fullwidth = True

    # Controls the visual order of fields listed.
    fields = (
        "affiliation_id",
        "expert_panel_id",
        "type",
        "full_name",
        "short_name",
        "status",
        "clinical_domain_working_group",
        "members",
    )
    inlines = [CoordinatorInlineAdmin, ApproverInlineAdmin, SubmitterInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        """Fields that are editable upon creation, afterwards, are read only"""
        # If the affiliation has not been created (is new) only return Members as read only
        # Otherwise, check to see if user has the staff role and is not a superuser,
        # Then return the full list of read only fields.
        # This allows superusers to edit these fields in the case of affiliation creation error.
        if obj is not None:
            if request.user.is_staff and not request.user.is_superuser:
                return [
                    "affiliation_id",
                    "expert_panel_id",
                    "type",
                    "members",
                ]
        return [
            "members",
        ]

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Customize visible fields in admin:
        - On add: hides affiliation_id and expert_panel_id
        - On change: show all fields
        """
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields["affiliation_id"].widget = forms.HiddenInput()
            form.base_fields["expert_panel_id"].widget = forms.HiddenInput()
        return form


# Add models we want to be able to edit in the admin interface.
admin.site.register(Affiliation, AffiliationsAdmin)

# Change the admin site's display name.
admin.site.site_title = "Affiliation Service"
admin.site.site_header = "Affiliation Service Panel"
admin.site.index_title = "Welcome to the ClinGen Affiliation Service Portal"
