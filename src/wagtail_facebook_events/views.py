from django.http import HttpResponse
from django.views.generic import TemplateView
from wagtail_facebook_events.service import FacebookEventsImporterService


class ImportEventsView(TemplateView):
    """View to import events from Facebook."""

    def get(self, request):
        service = FacebookEventsImporterService()
        service.import_events()
        return HttpResponse(service.import_events())
    

class EventsDashboardView(TemplateView):
    """View to display events dashboard."""

    template_name = "wagtail_facebook_events/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
