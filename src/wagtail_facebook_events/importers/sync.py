import logging
import time

from wagtail_facebook_events.importers import BaseFacebookEventsImporter

logger = logging.getLogger(__name__)


class FacebookEventsImporterSync(BaseFacebookEventsImporter):
    def __init__(self, full_sync=False):
        self.full_sync = full_sync
        logger.info(
            f"Initialized FacebookEventsImporterBase with full_sync={self.full_sync}"
        )

    def import_events(self):
        logger.info("Starting synchronous event import")
        start_time = time.time()
        events_page = self.events_api.get()
        create_events, update_events = [], []

        if self.full_sync:
            logger.info("Full sync enabled; fetching all pages")
            while events_page:
                new_create_events, new_update_events = self.processor.process_page(
                    events_page
                )
                create_events.extend(new_create_events)
                update_events.extend(new_update_events)
                next_url = events_page.get("paging", {}).get("next")
                if next_url:
                    logger.info(f"Fetching next page from URL: {next_url}")
                    events_page = self.events_api.fetch_next_page(next_url)
                else:
                    break
            logger.info(
                f"Creating {len(create_events)} events and updating {len(update_events)} events"
            )
        else:
            new_create_events, new_update_events = self.processor.process_page(
                events_page
            )
            create_events.extend(new_create_events)
            update_events.extend(new_update_events)
            logger.info(
                f"Creating {len(create_events)} events and updating {len(update_events)} events"
            )
        self.processor.bulk_create(create_events)
        self.processor.bulk_update(update_events)
        logger.info(
            f"Synchronous import finished in {time.time() - start_time:.2f} seconds"
        )
        return [event["id"] for event in create_events] + [
            event[1].facebook_id for event in update_events
        ]
