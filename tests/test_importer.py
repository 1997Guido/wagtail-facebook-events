import random
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from factory import Faker as FactoryFaker
from factory.django import DjangoModelFactory
from faker import Faker
from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file

from wagtail_facebook_events.importers import FacebookEventsImporterSync
from wagtail_facebook_events.models import Event

fake = Faker()
ImageModel = get_image_model()


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event


class CustomImageFactory(DjangoModelFactory):
    """
    Factory for creating CustomImage instances for testing.
    """

    class Meta:
        model = ImageModel

    title = FactoryFaker("name")
    file = get_test_image_file()


def generate_fake_event_data():
    """
    Generate a single fake event data dictionary.
    """
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S") + "+0000"
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S") + "+0000"
    event_id = random.randint(1000, 9999)

    return {
        "name": fake.name(),
        "description": fake.sentence(),
        "start_time": start_time_str,
        "end_time": end_time_str,
        "cover": {
            "offset_x": 50,
            "offset_y": 50,
            "source": fake.image_url(),
            "id": str(random.randint(1000, 9999)),
        },
        "place": {
            "name": fake.company(),
            "location": {
                "city": fake.city(),
                "country": fake.country(),
                "street": fake.street_address(),
                "zip": fake.zipcode(),
            },
        },
        "id": str(event_id),
    }


def generate_fake_events_data(num_events):
    """
    Generate a list of fake event data dictionaries.
    """
    events_data = []
    for _ in range(num_events):
        events_data.append(generate_fake_event_data())
    # check for duplicates
    for i in range(num_events):
        for j in range(i + 1, num_events):
            if events_data[i]["id"] == events_data[j]["id"]:
                events_data[j]["id"] = str(random.randint(1000, 9999))
    return events_data


def mock_save_event(self, *args, **kwargs):
    """
    Mock save method to call the original save method of the Django model.
    """
    super(Event, self).save(*args, **kwargs)


@pytest.mark.django_db
@pytest.mark.parametrize("num_events", [1, 5, 10])
def test_importer_with_fake_data(num_events):
    """
    Test importing a specified number of fake events.
    """
    fake_events_data = generate_fake_events_data(num_events)

    # Mock response for fetching event images
    mock_response = MagicMock()
    mock_response.read.return_value = b"fake_image_data"

    with patch(
        "kabelbreukevents.apps.facebook.facebook_importer.urlopen",
        return_value=mock_response,
    ), patch(
        "kabelbreukevents.apps.facebook.facebook_importer.FacebookEventsImporterSync._import_event_image",
        side_effect=lambda event: CustomImageFactory(),
    ), patch(
        "kabelbreukevents.apps.cms.models.Event.save", new=mock_save_event
    ):
        with patch.object(
            FacebookEventsImporterSync, "_get_events", return_value=fake_events_data
        ):
            importer = FacebookEventsImporterSync()
            importer.import_events()
            assert Event.objects.count() == num_events


@pytest.mark.django_db
def test_importer_with_empty_event_list():
    """
    Test importing an empty list of events.
    """
    empty_json = []

    with patch(
        "kabelbreukevents.apps.facebook.facebook_importer.FacebookEventsImporterSync._import_event_image",
        side_effect=lambda event: CustomImageFactory(),
    ), patch("kabelbreukevents.apps.cms.models.Event.save", new=mock_save_event):
        with patch.object(
            FacebookEventsImporterSync, "_get_events", return_value=empty_json
        ):
            importer = FacebookEventsImporterSync()
            importer.import_events()
            assert Event.objects.count() == 0


@pytest.mark.django_db
def test_importer_deduplication():
    """
    Test that importing the same events multiple times does not create duplicates.
    """
    fake_events_data = generate_fake_events_data(5)

    with patch(
        "kabelbreukevents.apps.facebook.facebook_importer.FacebookEventsImporterSync._import_event_image",
        side_effect=lambda event: CustomImageFactory(),
    ), patch("kabelbreukevents.apps.cms.models.Event.save", new=mock_save_event):
        with patch.object(
            FacebookEventsImporterSync, "_get_events", return_value=fake_events_data
        ):
            importer = FacebookEventsImporterSync()
            importer.import_events()  # First import
            importer.import_events()  # Second import with the same data
            assert (
                Event.objects.count() == 5
            )  # Count should not change because of deduplication logic


@pytest.mark.django_db
def test_update_if_changes():
    """
    Test that importing updated event data correctly updates the existing event.
    """
    with patch("kabelbreukevents.apps.cms.models.Event.save", new=mock_save_event):
        fake_events_data = generate_fake_events_data(1)
        event = EventFactory(id=fake_events_data[0]["id"])
        # Generate updated event data with the same ID but different name
        fake_events_data_updated = generate_fake_events_data(1)
        fake_events_data_updated[0]["id"] = event.id
        assert fake_events_data_updated[0]["id"] == event.id
    with patch(
        "kabelbreukevents.apps.facebook.facebook_importer.FacebookEventsImporterSync._import_event_image",
        side_effect=lambda event: CustomImageFactory(),
    ):
        with patch.object(
            FacebookEventsImporterSync,
            "_get_events",
            return_value=fake_events_data_updated,
        ):
            importer = FacebookEventsImporterSync()

            # this send the fake event data to the importer
            importer.import_events()
            # the event name should be updates, since a new event with the same ID but different name was imported
            event.refresh_from_db()
            assert event.title == fake_events_data_updated[0]["name"]
