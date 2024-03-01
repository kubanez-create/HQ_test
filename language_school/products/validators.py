from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_start_time(value):
    if value < timezone.now():
        raise ValidationError(
            "Start time must be in the future or, at least, now."
        )
