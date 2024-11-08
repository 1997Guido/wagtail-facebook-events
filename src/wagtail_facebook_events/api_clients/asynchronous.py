from typing import Any, Dict, List

import httpx

from wagtail_facebook_events.api_clients import BaseFacebookAPIClient


class FacebookEventsAPI(BaseFacebookAPIClient):
    async def get(self, fields: List[str] = None, limit: int = 25) -> Dict[str, Any]:
        """Asynchronously fetches a list of upcoming events with the specified fields and limit."""
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

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def fetch_next_page(self, next_url: str) -> Dict[str, Any]:
        """Asynchronously fetches the next page of events."""
        async with httpx.AsyncClient() as client:
            response = await client.get(next_url)
            response.raise_for_status()
            return response.json()
