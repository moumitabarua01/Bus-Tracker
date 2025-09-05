from django.urls import path
from . import views


app_name = "seatBokking"


urlpatterns = [
    path("", views.booking_home, name="home"),
    path("trip/<int:trip_id>/", views.booking_view, name="booking"),
    path("api/trip/<int:trip_id>/booked/", views.api_booked_seats, name="api_booked_seats"),
    path("api/trip/<int:trip_id>/book/", views.api_book_seat, name="api_book_seat"),
    path("admin/clear-bookings/", views.clear_all_bookings, name="clear_all_bookings"),
]


