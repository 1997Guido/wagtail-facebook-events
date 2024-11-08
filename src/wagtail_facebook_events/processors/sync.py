import logging
import time

from wagtail_facebook_events.processors import BaseEventsProcessor

logger = logging.getLogger(__name__)


class EventsProcessor(BaseEventsProcessor):
    def process_page(self, page):
        logger.info("Processing a page of events")
        start_time = time.time()
        events = page.get("data", [])
        create_events, update_events = [], []

        for event in events:
            create_event, update_event = self._create_or_update(event)
            if create_event:
                if create_event.get("cover", {}).get("source"):
                    create_event["image"] = self.image_processor.download(create_event)
                create_events.append(create_event)
            if update_event:
                new_data, instance = update_event
                if new_data.get("cover", {}).get("source"):
                    new_data["image"] = self.image_processor.download(new_data)
                update_events.append((new_data, instance))

        logger.info(f"Processed page in {time.time() - start_time:.2f} seconds")
        return create_events, update_events
