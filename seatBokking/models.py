from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date
import re

User = get_user_model()

def validate_seat_number(value):
    """Validate seat number format (e.g., '1A', '12B', '25C')."""
    if not re.match(r'^[1-9]\d?[A-Z]$', value):
        raise ValidationError('Seat number must be in format like 1A, 12B, 25C (number followed by letter).')

def validate_future_date(value):
    """Validate that the date is not in the past."""
    if value < date.today():
        raise ValidationError('Trip date cannot be in the past.')


class Trip(models.Model):
    name = models.CharField(
        max_length=128,
        validators=[RegexValidator(
            message='Trip name can only contain letters, numbers, spaces, hyphens, and underscores',
            regex=r'^[a-zA-Z0-9\s\-_]+$'
        )]
    )
    date = models.DateField(validators=[validate_future_date])
    arrival_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    departure_time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(decimal_places=2, default=0.0, max_digits=8)
    total_seats = models.PositiveIntegerField(default=50)
    updated_at = models.DateTimeField(auto_now=True)
    # New fields for trip details
    route = models.CharField(max_length=256, blank=True, null=True, help_text='Route of the bus trip')
    trip_time = models.CharField(max_length=64, blank=True, null=True, help_text='Time of the bus trip (e.g. 8:00 AM)')
    day = models.CharField(max_length=32, blank=True, null=True, help_text='Day of the trip (e.g. Monday)')

    class Meta:
        ordering = ['date', 'departure_time']
        indexes = [
            models.Index(fields=['date'], name='seatBokking_date_554814_idx'),
            models.Index(fields=['is_active'], name='seatBokking_is_acti_491f50_idx'),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.date})"


class SeatBooking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="bookings")
    seat_number = models.CharField(max_length=5, validators=[validate_seat_number])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seat_bookings")
    booked_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='confirmed'
    )

    class Meta:
        unique_together = ("trip", "seat_number")
        indexes = [
            models.Index(fields=['user'], name='seatBokking_user_id_90dda3_idx'),
            models.Index(fields=['status'], name='seatBokking_status_ae56c4_idx'),
            models.Index(fields=['booked_at'], name='seatBokking_booked__db39a4_idx'),
        ]

    def __str__(self) -> str:
        return f"{self.trip} - Seat {self.seat_number}"
