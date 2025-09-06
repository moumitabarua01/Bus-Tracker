from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

def validate_latitude(value):
    """Validate that latitude is between -90 and 90 degrees."""
    if not -90 <= value <= 90:
        raise ValidationError(f'Latitude must be between -90 and 90 degrees. Got {value}.')

def validate_longitude(value):
    """Validate that longitude is between -180 and 180 degrees."""
    if not -180 <= value <= 180:
        raise ValidationError(f'Longitude must be between -180 and 180 degrees. Got {value}.')

class BusLocation(models.Model):
    lat = models.FloatField(
        help_text='Latitude coordinate (-90 to 90 degrees)',
        validators=[validate_latitude]
    )
    lng = models.FloatField(
        help_text='Longitude coordinate (-180 to 180 degrees)',
        validators=[validate_longitude]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    bus_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Optional bus identifier'
    )
    direction = models.FloatField(
        blank=True,
        null=True,
        help_text='Direction in degrees (0-360, optional)',
        validators=[MinValueValidator(0), MaxValueValidator(360)]
    )
    speed = models.FloatField(
        blank=True,
        null=True,
        help_text='Speed in km/h (optional)',
        validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp'], name='tracker_bus_timesta_1e3195_idx'),
            models.Index(fields=['bus_id'], name='tracker_bus_bus_id_b7a20c_idx'),
        ]

    def __str__(self):
        return f"{self.lat}, {self.lng}"  # Convert float to string and include lng
