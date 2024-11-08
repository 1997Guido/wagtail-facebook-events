import hashlib
import logging
import time
from abc import ABC, abstractmethod
from wagtail.images import get_image_model

from wagtail_facebook_events import get_event_model, get_event_serializer
from wagtail_facebook_events.processors.image import EventImageProcessor

logger = logging.getLogger(__name__)


class BaseEventsProcessor(ABC):
    def __init__(self):
        self.EventModel = get_event_model()
        self.EventSerializer = get_event_serializer()
        self.image_model = get_image_model()
        self.image_processor = EventImageProcessor()

    @abstractmethod
    def process_page(self, page):
        pass

    def bulk_create(self, create_events):
        logger.info("Starting bulk create for events")
        start_time = time.time()
        create_serializer = self.EventSerializer(data=create_events, many=True)
        if create_serializer.is_valid():
            instances = [
                self.EventModel(**data) for data in create_serializer.validated_data
            ]
            self.EventModel.objects.bulk_create(instances)
            logger.info(
                f"Bulk created {len(instances)} events in {time.time() - start_time:.2f} seconds"
            )
        else:
            logger.info(f"Bulk create failed: {create_serializer.errors}")

    def bulk_update(self, update_events):
        logger.info("Starting bulk update for events")
        start_time = time.time()
        update_instances = []

        for data, instance in update_events:
            serializer = self.EventSerializer(instance, data=data, partial=False)
            if serializer.is_valid():
                for field, value in serializer.validated_data.items():
                    setattr(instance, field, value)
                update_instances.append(instance)
            else:
                logger.info(
                    f"Could not update event {instance.id}: {serializer.errors}"
                )

        if update_instances:
            self.EventModel.objects.bulk_update(
                update_instances,
                fields=[
                    field.name
                    for field in self.EventModel._meta.fields
                    if not field.primary_key
                ],
            )
            logger.info(
                f"Bulk updated {len(update_instances)} events in {time.time() - start_time:.2f} seconds"
            )

    def _create_or_update(self, json_event):
        event_id = json_event.get("id")
        event_hash = self._hash(json_event)
        logger.info(f"Processing event {event_id}")

        if self.EventModel.objects.filter(facebook_id=event_id).exists():
            event_in_db = self.EventModel.objects.get(facebook_id=event_id)
            if event_hash != event_in_db.hashed and not event_in_db.stop_import:
                json_event["hashed"] = event_hash
                logger.info(f"Event {event_id} requires an update")
                return None, (json_event, event_in_db)
        else:
            json_event["hashed"] = event_hash
            logger.info(f"Event {event_id} will be created")
            return json_event, None

        logger.info(f"Event {event_id} did not change; skipping")
        return None, None

    @staticmethod
    def _hash(event) -> str:
        included_fields = [
            "id",
            "name",
            "description",
            "start_time",
            "end_time",
            "place",
        ]
        hash_string = "".join(
            f"{key}:{value}" for key, value in event.items() if key in included_fields
        )
        return hashlib.sha256(hash_string.encode()).hexdigest()
