from django.conf import settings


def get_setting(name: str, default=None):
    return getattr(settings, "WAGTAIL_FACEBOOK_EVENTS_%s" % name, default)


IMPORTER = get_setting(
    "IMPORTER", "wagtail_facebook_events.importers.sync.FacebookEventsImporterSync"
)
EVENT_MODEL = get_setting("EVENT_MODEL", "wagtail_facebook_events.FacebookEvent")
EVENT_SERIALIZER = get_setting(
    "EVENT_SERIALIZER", "wagtail_facebook_events.serializers.FacebookEventSerializer"
)
ACCESS_TOKEN = get_setting("ACCESS_TOKEN", "")
APP_ID = get_setting("APP_ID", "")
APP_SECRET = get_setting("APP_SECRET", "")
PAGE_ID = get_setting("PAGE_ID", "")
FULL_SYNC = get_setting("FULL_SYNC", False)
