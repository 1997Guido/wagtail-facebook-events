import re
from datetime import datetime

from rest_framework import serializers

from wagtail_facebook_events import get_event_model

class FacebookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_event_model()
        fields = [
            "facebook_id",
            "hashed",
            "stop_import",
            "name",
            "date",
            "image",
            "start_time",
            "end_time",
            "price",
            "is_free",
            "venue",
            "street",
            "city",
            "zip_code",
            "country",
            "latitude",
            "longitude",
            "place",
            "description",
            "url",
            "ticket_url",
        ]
        abstract = True

    def to_internal_value(self, data):
        data = self.transform_data(data)
        return super().to_internal_value(data)

    def transform_data(self, data: dict) -> dict:
        data["facebook_id"] = data.get("id")
        data["hashed"] = data.get("hashed")
        if data.get("start_time"):
            start_datetime = self._parse_datetime(data["start_time"])
            if start_datetime:
                data["date"] = start_datetime.date()
                data["start_time"] = start_datetime.time()
        if data.get("end_time"):
            end_datetime = self._parse_datetime(data["end_time"])
            if end_datetime and isinstance(end_datetime, datetime):
                data["end_time"] = end_datetime.time()
        data["url"] = f"https://www.facebook.com/events/{data.get('id')}/"
        data["ticket_url"] = data.get("ticket_uri")
        if data.get("description"):
            data["description"] = self._convert_unicode_description(data["description"])
        if data.get("place"):
            data["venue"] = data["place"].get("name")
            data["street"] = data["place"].get("location", {}).get("street")
            data["city"] = data["place"].get("location", {}).get("city")
            data["zip_code"] = data["place"].get("location", {}).get("zip")
            data["country"] = data["place"].get("location", {}).get("country")
            data["latitude"] = data["place"].get("location", {}).get("latitude")
            data["longitude"] = data["place"].get("location", {}).get("longitude")
        return data

    @staticmethod
    def _parse_datetime(datetime_str):
        """Parse a datetime string and return a datetime object."""
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            return None

    @staticmethod
    def _parse_time(datetime_str):
        try:
            dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
            return dt.time()
        except ValueError:
            return None

    @staticmethod
    def _convert_unicode_description(description: str):
        # Convert URLs into clickable links
        url_pattern = re.compile(r"(https?://[^\s]+)")
        description = url_pattern.sub(
            r'<a href="\1" target="_blank">\1</a>', description
        )

        # Preserve newlines in description
        description = description.replace("\n", "<br>")

        return description
