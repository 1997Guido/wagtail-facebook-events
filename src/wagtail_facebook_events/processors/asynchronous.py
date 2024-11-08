import asyncio
import logging
import time

from asgiref.sync import sync_to_async

from wagtail_facebook_events.processors import BaseEventsProcessor
from wagtail_facebook_events.processors.image import AsyncEventImageProcessor

logger = logging.getLogger(__name__)


class AsyncEventsProcessor(BaseEventsProcessor):
    def __init__(self):
        super().__init__()
        self.image_processor = AsyncEventImageProcessor()

    async def process_page(self, page):
        """Process each event page, downloading and saving images concurrently."""
        logger.info("Processing a page of events asynchronously")
        start_time = time.time()
        events = page.get("data", [])
        create_events, update_events = [], []
        image_tasks = []

        for event in events:
            create_event, update_event = await sync_to_async(self._create_or_update)(
                event
            )
            if create_event:
                create_events.append(create_event)
                if create_event.get("cover", {}).get("source"):
                    image_tasks.append(self.image_processor.download(create_event))
            if update_event:
                update_events.append(update_event)
                if update_event[0].get("cover", {}).get("source"):
                    image_tasks.append(self.image_processor.download(update_event[0]))

        # Await all download and save tasks to complete
        saved_images = await asyncio.gather(*image_tasks)
        logger.info(
            f"Finished processing page in {time.time() - start_time:.2f} seconds"
        )
        return create_events, update_events
