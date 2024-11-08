import logging
from abc import ABC, abstractmethod

from wagtail_facebook_events.api_clients.sync import FacebookEventsAPI
from wagtail_facebook_events.processors.sync import EventsProcessor

logger = logging.getLogger(__name__)


class BaseFacebookEventsImporter(ABC):
    events_api = FacebookEventsAPI()
    processor = EventsProcessor()
    full_sync = False

    @abstractmethod
    def import_events(self):
        pass
