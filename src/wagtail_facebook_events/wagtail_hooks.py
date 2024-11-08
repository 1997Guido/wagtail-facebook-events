from django.urls import path
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail_facebook_events.views import ImportEventsView


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("import-events/", ImportEventsView.as_view(), name="import_events"),
    ]


@hooks.register("register_admin_menu_item")
def register_import_events_menu_item():
    return MenuItem(
        "Import Events",
        "/admin/import-events/",
        icon_name="date",
        order=10000,
    )
