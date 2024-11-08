import random
from datetime import timedelta
from typing import Any, Dict, List

from asgiref.sync import sync_to_async
from django.utils import timezone
from faker import Faker

from wagtail_facebook_events.api_clients import BaseFacebookAPIClient

fake = Faker()


class FakeFacebookEventsAPI(BaseFacebookAPIClient):
    def __init__(self):
        super().__init__()
        # Initialize a counter for pagination tracking
        self.page_counter = 0

    def get(self, fields: List[str] = None, limit: int = 25) -> Dict[str, Any]:
        """Returns a list of fake events with the specified fields and limit."""
        return generate_fake_events_data_with_next_page(limit, next_page=True)

    def fetch_next_page(self, next_url: str) -> Dict[str, Any]:
        """Fetches the next page of fake events, stops after 10 calls."""
        self.page_counter += 1
        next_page = self.page_counter < 50
        return generate_fake_events_data_with_next_page(50, next_page=next_page)

    async def async_get(
        self, fields: List[str] = None, limit: int = 25
    ) -> Dict[str, Any]:
        """Asynchronously fetches a list of fake events with the specified fields and limit."""
        return await sync_to_async(generate_fake_events_data_with_next_page)(
            limit, next_page=True
        )

    async def async_fetch_next_page(self, next_url: str) -> Dict[str, Any]:
        """Asynchronously fetches the next page of fake events, stops after 10 calls."""
        self.page_counter += 1
        next_page = self.page_counter < 50
        return await sync_to_async(generate_fake_events_data_with_next_page)(
            50, next_page=next_page
        )


def generate_fake_event_data():
    """Generate a single fake event data dictionary."""
    start_time = timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = (timezone.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    event_id = random.randint(1000, 9999)
    return {
        "name": fake.name(),
        "description": fake.sentence(),
        "start_time": start_time,
        "end_time": end_time,
        "place": {"name": fake.company(), "location": {"city": fake.city()}},
        "cover": {
            "source": "https://images.unsplash.com/photo-1720048171098-dba33b2c4806?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        "id": str(event_id),
    }


def generate_fake_events_data(num_events):
    """Generate a list of fake event data dictionaries."""
    return [generate_fake_event_data() for _ in range(num_events)]


def generate_fake_events_data_with_next_page(num_events, next_page=False):
    """Generate a list of fake event data dictionaries with a next page URL."""
    if not next_page:
        return {"data": generate_fake_events_data(num_events)}
    return {
        "data": generate_fake_events_data(num_events),
        "paging": {"next": "next_page_url"},
    }
