from django.urls import path
from wagtail_facebook_events.views import ImportEventsView

app_name = "wagtail_facebook_events"

url_patterns = [
        path("import-events/", ImportEventsView.as_view(), name="import_events"),
    ]