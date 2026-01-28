from datetime import date
from .models import Booking

def auto_complete_bookings():
    Booking.objects.filter(
        booking_date__lt=date.today(),
        status='accepted'
    ).update(status='completed')
