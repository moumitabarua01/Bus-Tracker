from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Trip(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.name} ({self.date})"


class SeatBooking(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="bookings")
    seat_number = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seat_bookings")
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trip", "seat_number")

    def __str__(self) -> str:
        return f"{self.trip} - Seat {self.seat_number}"
