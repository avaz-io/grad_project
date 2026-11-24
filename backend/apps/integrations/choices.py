from django.db import models


class ZoomStatus(models.TextChoices):
    """Where a Zoom meeting is in its life. Used by live lectures and bookings.

    `failed` rows are picked up again later, so a Zoom outage never breaks
    a booking or a lecture (FR-ZOOM-04).
    """

    NONE = "none", "Not created"
    CREATED = "created", "Created"
    FAILED = "failed", "Failed (will retry)"
