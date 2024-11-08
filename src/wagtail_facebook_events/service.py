from wagtail_facebook_events import get_importer


class FacebookEventsImporterService:
    def __init__(self):
        self.importer = get_importer()

    def import_events(self):
        return self.importer.import_events()
