from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.fields import RichTextField


class FacebookEvent(models.Model):
    """FacebookEvent model."""

    facebook_id = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text=_("ID of the FacebookEvent"),
        default="",
    )
    hashed = models.CharField(blank=True, null=True)
    stop_import = models.BooleanField(
        default=False,
        help_text=_(
            "Check this if you no longer want this FacebookEvent to update from Facebook."
        ),
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text=_("Name of the FacebookEvent"),
        default="",
    )
    date = models.DateField(
        blank=False, null=True, help_text=_("Date of the FacebookEvent")
    )
    image = models.ForeignKey(
        "cms.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Image of the FacebookEvent"),
    )
    start_time = models.TimeField(
        blank=False, null=True, help_text=_("Start time of the FacebookEvent")
    )
    end_time = models.TimeField(
        blank=False, null=True, help_text=_("End time of the FacebookEvent")
    )
    price = models.CharField(
        max_length=255, blank=True, null=True, help_text=_("Price of the FacebookEvent")
    )
    is_free = models.BooleanField(
        default=True, help_text=_("Is the FacebookEvent free?")
    )
    venue = models.CharField(
        max_length=255, blank=True, null=True, help_text=_("Venue of the FacebookEvent")
    )
    street = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Street of the FacebookEvent"),
    )
    city = models.CharField(
        max_length=255, blank=True, null=True, help_text=_("City of the FacebookEvent")
    )
    zip_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Zip code of the FacebookEvent"),
    )
    country = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Country of the FacebookEvent"),
    )
    latitude = models.FloatField(
        blank=True, null=True, help_text=_("Latitude of the FacebookEvent")
    )
    longitude = models.FloatField(
        blank=True, null=True, help_text=_("Longitude of the FacebookEvent")
    )
    place = models.JSONField(
        blank=True,
        null=True,
        help_text=_("Place of the FacebookEvent (JSON from Facebook)"),
    )
    description = RichTextField(
        blank=True, null=True, help_text=_("Description of the FacebookEvent")
    )
    url = models.URLField(
        blank=True, null=True, help_text=_("URL of the FacebookEvent")
    )
    ticket_url = models.URLField(
        blank=True, null=True, help_text=_("URL of the ticket")
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date"]
        verbose_name = _("FacebookEvent")
        abstract = True
