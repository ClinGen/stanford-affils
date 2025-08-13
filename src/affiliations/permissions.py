"""Custom API permissions."""

from rest_framework_api_key.permissions import BaseHasAPIKey
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.utils.timezone import now
from affiliations.models import CustomAPIKey


class HasWriteAccess(BasePermission):
    """
    Custom permission that checks if a provided API key has `can_write=True`.
    """

    model = CustomAPIKey

    def has_permission(self, request, view):
        """Checks permissions and raises PermissionDenied if invalid."""
        raw_key = request.META.get("HTTP_X_API_KEY")
        if not raw_key:
            raise PermissionDenied("No API key was provided in the request headers.")

        api_key_obj = CustomAPIKey.objects.get_from_key(raw_key)
        if not api_key_obj:
            raise PermissionDenied("The provided API key is invalid.")

        if api_key_obj.revoked:
            raise PermissionDenied("The provided API key has been revoked.")

        if api_key_obj.expiry_date and api_key_obj.expiry_date < now():
            raise PermissionDenied("The provided API key has expired.")

        if not api_key_obj.can_write:
            raise PermissionDenied("The API key does not have write permissions.")

        return True


class HasAffilsAPIKey(BaseHasAPIKey):
    """
    Custom permission that checks if a provided API key is valid.
    """

    model = CustomAPIKey
