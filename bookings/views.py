from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from .models import TravelPackage, Booking, DocumentReminder
from destinations.models import Destination

@login_required
def book_package(request, package_id):
    package = get_object_or_404(TravelPackage, pk=package_id)

    if request.method == 'POST':
        travel_date = request.POST.get('travel_date')
        guests = int(request.POST.get('number_of_people', 1))
        total_price = package.price * guests
        voucher = f"TM-{random.randint(10000, 99999)}"

        booking = Booking.objects.create(
            user=request.user,
            package=package,
            destination=package.destination,
            travel_date=travel_date,
            number_of_people=guests,
            total_amount=total_price,
            status='Confirmed',
            voucher_code=voucher
        )
        messages.success(request, f"Booking #{booking.id} confirmed successfully! Voucher: {voucher}")
        return redirect('voucher_detail', booking_id=booking.id)

    return render(
        request,
        'bookings/book_package.html',
        {
            'package': package,
        }
    )

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    reminders = DocumentReminder.objects.filter(user=request.user)
    return render(
        request,
        'bookings/booking_history.html',
        {
            'bookings': bookings,
            'reminders': reminders
        }
    )

@login_required
def voucher_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(
        request,
        'bookings/voucher_detail.html',
        {
            'booking': booking
        }
    )
