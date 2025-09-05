from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from .models import Trip, SeatBooking
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now
from django.contrib.admin.views.decorators import staff_member_required


def booking_home(request):
    trips = Trip.objects.order_by("date")
    if not trips.exists():
        # seed default trips for convenience
        from datetime import date
        Trip.objects.create(name="Ronobheri", date=date.today())
        Trip.objects.create(name="Bhorer Alo", date=date.today())
        trips = Trip.objects.order_by("date")
    return render(request, "seatBokking/home.html", {"trips": trips})


@ensure_csrf_cookie
@login_required
def booking_view(request, trip_id: int):
    trip = get_object_or_404(Trip, id=trip_id)
    existing = SeatBooking.objects.filter(trip=trip, user=request.user).first()
    return render(
        request,
        "seatBokking/booking.html",
        {"trip": trip, "is_authenticated": request.user.is_authenticated, "existing_booking": existing},
    )


def api_booked_seats(request, trip_id: int):
    trip = get_object_or_404(Trip, id=trip_id)
    booked = list(SeatBooking.objects.filter(trip=trip).values_list("seat_number", flat=True))
    return JsonResponse({"booked": booked})


@login_required
@require_POST
def api_book_seat(request, trip_id: int):
    trip = get_object_or_404(Trip, id=trip_id)
    seat = request.POST.get("seat")
    if not seat:
        return HttpResponseBadRequest("Missing seat")
    # Enforce: one seat per user per trip
    if SeatBooking.objects.filter(user=request.user, trip=trip).exists():
        return JsonResponse({"ok": False, "error": "You already booked a seat for this trip."}, status=400)
    # Try create booking
    try:
        booking = SeatBooking.objects.create(trip=trip, seat_number=seat, user=request.user)
        
        # Send email confirmation
        try:
            subject = f'Seat Booking Confirmation - {trip.name}'
            message = f'''
Dear {request.user.first_name or request.user.username},

Your seat booking has been confirmed!

Trip: {trip.name}
Date: {trip.date}
Seat Number: {seat}
Booking Time: {booking.booked_at.strftime('%Y-%m-%d %H:%M:%S')}

Thank you for choosing our bus service.

Best regards,
Bus Tracker Team
            '''
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log error but don't fail the booking
            print(f"Email sending failed: {e}")
            
    except Exception:
        return JsonResponse({"ok": False, "error": "Seat already booked"}, status=400)
    return JsonResponse({"ok": True})


@staff_member_required
def clear_all_bookings(request):
    if request.method == "POST":
        SeatBooking.objects.all().delete()
        return JsonResponse({"ok": True, "message": "All bookings cleared"})
    return JsonResponse({"ok": False, "error": "POST required"}, status=405)

# Create your views here.
