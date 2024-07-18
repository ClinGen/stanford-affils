"""Define custom renderers for the affiliations service."""

# Third-party dependencies:
from rest_framework.renderers import BrowsableAPIRenderer


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable API, but excludes the forms.

    There's a setting in the project-level settings module that makes
    Django REST Framework use this renderer by default.
    """

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        ctx["display_edit_forms"] = False
        return ctx

    def show_form_for_method(self, view, method, request, obj):
        """We never want to do this; just return false."""
        return False

    def get_rendered_html_form(self, data, view, method, request):
        """This method normally returns rendered HTML."""
        return ""
