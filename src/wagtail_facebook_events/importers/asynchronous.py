import asyncio
import logging
import time

from asgiref.sync import sync_to_async

from wagtail_facebook_events.importers import BaseFacebookEventsImporter
from wagtail_facebook_events.processors.asynchronous import (
    AsyncEventsProcessor,
)

logger = logging.getLogger(__name__)


class FacebookEventsImporterAsync(BaseFacebookEventsImporter):
    def __init__(self, full_sync=False):
        self.full_sync = full_sync
        self.processor = AsyncEventsProcessor()
        logger.info(
            f"Initialized FacebookEventsImporterBase with full_sync={self.full_sync}"
        )

    async def import_events(self):
        logger.info("Starting asynchronous event import")
        start_time = time.time()
        events_page = await self.events_api.async_get()
        create_events, update_events = [], []
        if self.full_sync:
            logger.info("Full sync enabled; fetching all pages")
            while events_page:
                next_url = events_page.get("paging", {}).get("next")
                next_page_task = (
                    asyncio.create_task(self.events_api.async_fetch_next_page(next_url))
                    if next_url
                    else None
                )

                (
                    new_create_events,
                    new_update_events,
                ) = await self.processor.process_page(events_page)
                create_events.extend(new_create_events)
                update_events.extend(new_update_events)

                events_page = await next_page_task if next_page_task else None
            logger.info(
                f"Creating {len(create_events)} events and updating {len(update_events)} events"
            )
        else:
            new_create_events, new_update_events = await self.processor.process_page(
                events_page
            )
            create_events.extend(new_create_events)
            update_events.extend(new_update_events)
            logger.info(
                f"Creating {len(create_events)} events and updating {len(update_events)} events"
            )
        await sync_to_async(self.processor.bulk_create)(create_events)
        await sync_to_async(self.processor.bulk_update)(update_events)
        logger.info(
            f"Asynchronous import finished in {time.time() - start_time:.2f} seconds"
        )
        return [event["id"] for event in create_events] + [
            event[1].facebook_id for event in update_events
        ]
