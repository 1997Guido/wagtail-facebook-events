from abc import ABC, abstractmethod

from wagtail_facebook_events.settings import (
    ACCESS_TOKEN,
    APP_ID,
    APP_SECRET,
    PAGE_ID,
)


class BaseFacebookAPIClient(ABC):
    access_token = ACCESS_TOKEN
    app_id = APP_ID
    app_secret = APP_SECRET
    page_id = PAGE_ID

    @abstractmethod
    def get():
        pass

    @abstractmethod
    def fetch_next_page():
        pass
