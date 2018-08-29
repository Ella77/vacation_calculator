from django.views.generic import TemplateView
from django_popup_view_field.registry import registry_popup_view


class PopupView(TemplateView):
    template = 'popups/popup.hrml'


registry_popup_view.register(PopupView)
