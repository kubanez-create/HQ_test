from datetime import datetime
from django.core.exceptions import ValidationError


def validate_start_time(value):
    if value < datetime.now():
        raise ValidationError(
            "Start time must be in the future or, at least, now."
        )
