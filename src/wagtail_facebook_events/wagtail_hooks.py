from django.urls import path
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail_facebook_events.views import EventsDashboardView, ImportEventsView
from django.conf import settings


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("events-dashboard/", EventsDashboardView.as_view(), name="events_dashboard"),
        path("import-events/", ImportEventsView.as_view(), name="import_events"),
    ]


@hooks.register("register_admin_menu_item")
def register_import_events_menu_item():
    return MenuItem(
        "events-dashboard",
        "/" + settings.WAGTAIL_ADMIN_URL + "events-dashboard/",
        icon_name="date",
        order=10000,
    )
