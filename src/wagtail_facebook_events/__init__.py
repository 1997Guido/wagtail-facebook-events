from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from wagtail_facebook_events.settings import (
    EVENT_MODEL,
    EVENT_SERIALIZER,
    IMPORTER,
)


def get_event_model():
    try:
        return import_string(EVENT_MODEL)
    except ImportError:
        raise ImproperlyConfigured(
            f"Could not import event model {EVENT_MODEL}. Is it correct?"
        )


def get_event_serializer():
    try:
        return import_string(EVENT_SERIALIZER)
    except ImportError:
        raise ImproperlyConfigured(
            f"Could not import event serializer {EVENT_SERIALIZER}. Is it correct?"
        )


def get_importer():
    try:
        return import_string(IMPORTER)()
    except ImportError:
        raise ImproperlyConfigured(
            f"Could not import importer {IMPORTER}. Is it correct?"
        )
