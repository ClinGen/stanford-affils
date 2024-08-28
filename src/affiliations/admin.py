"""Admin config for the affiliations service."""

# Third-party dependencies:
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

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


class AffiliationForm(forms.ModelForm):
    """Create forms to display information in Admin page."""

    class Meta:
        """Meta class for forms"""

        fields = "__all__"
        model = Affiliation

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
            _type
            in (
                "SC_VCEP",
                "INDEPENDENT_CURATION",
            )
            and ep_id is not None
        ):
            self.add_error(
                "expert_panel_id",
                ValidationError(
                    "If type Independent Curation Group or SC-VCEP is selected, "
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
        if _type == "GCEP":
            if ep_id is None or (ep_id < 40000 or ep_id >= 50000):
                self.add_error(
                    "expert_panel_id",
                    ValidationError(
                        "Valid GCEP ID's should be in the 40000 number range. "
                        "Please include a valid Expert Panel ID."
                    ),
                )
            elif affil_id - 10000 != ep_id - 40000:
                self.add_error(
                    None,
                    ValidationError(
                        "The Affiliation ID and Expert Panel ID do not match."
                    ),
                )
        if _type == "VCEP":
            if ep_id is None or (ep_id < 50000 or ep_id >= 60000):
                self.add_error(
                    "expert_panel_id",
                    ValidationError(
                        "Valid VCEP ID's should be in the  50000 number range. "
                        "Please include a valid Expert Panel ID."
                    ),
                )
            elif affil_id - 10000 != ep_id - 50000:
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

    # Controls which fields are searchable via the search bar.
    search_fields = [
        "affiliation_id",
        "expert_panel_id",
        "full_name",
        "abbreviated_name",
    ]

    # Controls what fields are listed in overview header.
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

    # Controls what columns are "clickable" to enter detailed view.
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
        "abbreviated_name",
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
                    "clinical_domain_working_group",
                    "members",
                ]
        return [
            "members",
        ]


# Add models we want to be able to edit in the admin interface.
admin.site.register(Affiliation, AffiliationsAdmin)

# Change the admin site's display name.
admin.site.site_title = "Affils Service"
admin.site.site_header = "Affiliation Service Panel"
admin.site.index_title = "Welcome to the ClinGen Affiliation Service Portal"
