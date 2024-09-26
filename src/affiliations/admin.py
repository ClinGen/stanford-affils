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

    def _handle_clean_affiliation_id(self, cleaned_data):
        """Clean and set Affiliation ID based on affil ID type."""
        affil_id = cleaned_data.get("affiliation_id")

        existing_affil_ids = (
            Affiliation.objects.select_for_update()
            .values_list("affiliation_id", flat=True)
            .order_by("affiliation_id")
        )

        last_ind = existing_affil_ids.count()
        if last_ind:
            affil_id = existing_affil_ids[last_ind - 1] + 1
        else:
            affil_id = 10000
        cleaned_data["affiliation_id"] = affil_id
        if affil_id < 10000 or affil_id >= 20000:
            self.add_error(
                None,
                ValidationError("Affiliation ID out of range. Contact administrator."),
            )

    def _handle_clean_type(self, cleaned_data):
        """Clean and set EP ID based on Type and Affiliation ID."""
        affil_id = cleaned_data.get("affiliation_id")
        ep_id = cleaned_data.get("expert_panel_id")
        _type = cleaned_data.get("type")

        if _type == "VCEP":
            ep_id = (affil_id - 10000) + 50000
            cleaned_data["expert_panel_id"] = ep_id
            if ep_id < 50000 or ep_id >= 60000:
                self.add_error(
                    None,
                    ValidationError("VCEP ID out of range. Contact administrator."),
                )
        elif _type == "SC_VCEP":
            ep_id = (affil_id - 10000) + 50000
            cleaned_data["expert_panel_id"] = ep_id
            cleaned_data["clinical_domain_working_group"] = "SOMATIC_CANCER"
            if ep_id < 50000 or ep_id >= 60000:
                self.add_error(
                    None,
                    ValidationError("SC-VCEP ID out of range. Contact administrator."),
                )
        elif _type == "GCEP":
            ep_id = (affil_id - 10000) + 40000
            cleaned_data["expert_panel_id"] = ep_id
            if ep_id < 40000 or ep_id >= 50000:
                self.add_error(
                    None,
                    ValidationError("GCEP ID out of range. Contact administrator."),
                )
        else:
            cleaned_data["expert_panel_id"] = None

    @transaction.atomic
    def clean(self):
        cleaned_data = super().clean()
        # If the primary key already exists, return cleaned_data.
        if self.instance.pk is not None:
            return cleaned_data

        self._handle_clean_affiliation_id(cleaned_data)
        self._handle_clean_type(cleaned_data)

        # Check to see if the Affil and EP ID already exist in DB.
        if (
            Affiliation.objects.select_for_update()
            .filter(
                affiliation_id=cleaned_data.get("affiliation_id"),
                expert_panel_id=cleaned_data.get("expert_panel_id"),
            )
            .exists()
        ):
            self.add_error(
                None,
                ValidationError(
                    "This Affiliation ID with this Expert Panel ID already exist."
                ),
            )

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


class AffiliationsAdmin(ModelAdmin):
    """Configure the affiliations admin panel."""

    form = AffiliationForm

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
                    "clinical_domain_working_group",
                    "members",
                ]
        return [
            "members",
        ]

    def render_change_form(self, request, context, *args, obj=None, **kwargs):
        if obj is None:
            context["media"] += forms.Media(
                js=["js/admin_hide_attribute_new.js"],
            )
        return super().render_change_form(request, context, *args, obj=None, **kwargs)


# Add models we want to be able to edit in the admin interface.
admin.site.register(Affiliation, AffiliationsAdmin)

# Change the admin site's display name.
admin.site.site_title = "Affiliation Service"
admin.site.site_header = "Affiliation Service Panel"
admin.site.index_title = "Welcome to the ClinGen Affiliation Service Portal"
