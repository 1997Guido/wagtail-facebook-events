import asyncio
import logging
import time

from celery import shared_task

from wagtail_facebook_events.importers.asynchronous import (
    FacebookEventsImporterAsync,
)
from wagtail_facebook_events.processors.asynchronous import (
    AsyncEventsProcessor,
)

logger = logging.getLogger(__name__)


class CeleryFacebookEventsImporterAsync(FacebookEventsImporterAsync):
    # WIP

    async def import_events(self):
        logger.info("Starting asynchronous event import with Celery")
        start_time = time.time()
        events_page = await self.events_api.async_get()

        # List to store async task results for each page
        tasks = []

        if self.full_sync:
            logger.info("Full sync enabled; fetching all pages")
            while events_page:
                # Add a task to Celery for processing the current page
                task = process_page_task.delay(events_page)
                tasks.append(task)

                # Fetch the next page asynchronously
                next_url = events_page.get("paging", {}).get("next")
                events_page = (
                    await self.events_api.async_fetch_next_page(next_url)
                    if next_url
                    else None
                )
        else:
            # Process a single page if full sync is not enabled
            task = process_page_task.delay(events_page)
            tasks.append(task)

        # Collect all results once tasks are done
        create_events_ids, update_events_ids = [], []
        for task in tasks:
            result = task.get()  # Retrieve task result
            create_events_ids.extend(result.get("created", []))
            update_events_ids.extend(result.get("updated", []))

        logger.info(
            f"Finished asynchronous import with Celery in {time.time() - start_time:.2f} seconds"
        )

        return create_events_ids + update_events_ids


@shared_task
def process_page_task(events_page):
    # WIP
    """
    Celery task to process a single page of events.
    """
    processor = AsyncEventsProcessor()  # Use the async processor
    new_create_events, new_update_events = asyncio.run(
        processor.process_page(events_page)
    )

    # Bulk create and update within the task
    processor.bulk_create(new_create_events)
    processor.bulk_update(new_update_events)

    return {
        "created": [event["id"] for event in new_create_events],
        "updated": [event[1].facebook_id for event in new_update_events],
    }
