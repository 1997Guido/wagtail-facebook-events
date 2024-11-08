from typing import Any, Dict, List

import httpx
import requests

from wagtail_facebook_events.api_clients import BaseFacebookAPIClient


class FacebookEventsAPI(BaseFacebookAPIClient):
    def get(self, fields: List[str] = None, limit: int = 25) -> Dict[str, Any]:
        """Returns a list of upcoming events with the specified fields and limit."""
        if fields is None:
            fields = [
                "name",
                "description",
                "date",
                "start_time",
                "end_time",
                "cover",
                "place",
                "ticket_uri",
            ]

        fields_query = ",".join(fields)

        url = f"https://graph.facebook.com/v20.0/{self.page_id}/events"
        params = {
            "access_token": self.access_token,
            "fields": fields_query,
            "limit": limit,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        events_page = response.json()
        return events_page

    def fetch_next_page(self, next_url: str) -> Dict[str, Any]:
        """Fetches the next page of events."""
        response = requests.get(next_url)
        response.raise_for_status()
        events_page = response.json()
        return events_page
