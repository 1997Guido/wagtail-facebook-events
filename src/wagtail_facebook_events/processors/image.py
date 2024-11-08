import logging
import time
from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile
from typing import Optional
from urllib.request import urlopen

import httpx
from django.core.files import File
from wagtail.images import get_image_model

logger = logging.getLogger(__name__)

class BaseImageProcessor(ABC):
    image_model = get_image_model()

    @abstractmethod
    def download(self, url):
        pass

class EventImageProcessor(BaseImageProcessor):
    def download(self, event) -> Optional[int]:
        logger.info(f"Downloading image for event {event.get('id')}")
        start_time = time.time()
        response = urlopen(event["cover"]["source"])
        image_temp = NamedTemporaryFile(delete=True)
        image_temp.write(response.read())
        image_temp.flush()
        image_model = get_image_model()
        name = event["name"]
        image, created = image_model.objects.get_or_create(
            title=name,
            file=File(image_temp, name=f"{name}.jpg"),
        )
        logger.info(
            f"Downloaded and saved image for event {event.get('id')} in {time.time() - start_time:.2f} seconds"
        )
        return image.pk


class AsyncEventImageProcessor(BaseImageProcessor):
    async def download(self, event):
        """Downloads the image and immediately saves it to the database."""
        logger.info(f"Downloading image for event {event.get('id')}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(event["cover"]["source"])
                response.raise_for_status()

                image_temp = NamedTemporaryFile(delete=True)
                image_temp.write(response.content)
                image_temp.flush()

                # As soon as download completes, save the image to the database
                return await self._save_image(image_temp, event)
        except httpx.HTTPError as e:
            logger.error(f"Failed to download image for event {event.get('id')}: {e}")
            return None, event.get("id")

    async def _save_image(self, image_temp, event):
        """Save the downloaded image to the database."""
        name = event["name"]
        image_model = self.image_model

        image, created = await image_model.objects.aget_or_create(
            title=name,
            file=File(image_temp, name=f"{name}.jpg"),
        )
        image_temp.close()
        event["image"] = image.pk
        return image.pk
