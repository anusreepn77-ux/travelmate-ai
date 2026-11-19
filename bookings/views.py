from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import random
from .models import TravelPackage, Booking, DocumentReminder
from destinations.models import Destination
from recomendations.ml_engine import calculate_route_matrix

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

@login_required
def add_document_reminder(request):
    """Utility Feature B: Travel Document Reminder."""
    if request.method == 'POST':
        doc_type = request.POST.get('document_type')
        doc_number = request.POST.get('document_number', '')
        expiry = request.POST.get('expiry_date') or None
        notes = request.POST.get('notes', '')

        DocumentReminder.objects.create(
            user=request.user,
            document_type=doc_type,
            document_number=doc_number,
            expiry_date=expiry,
            notes=notes,
            is_verified=True
        )
        messages.success(request, f"Document reminder for '{doc_type}' created!")
    return redirect('booking_history')

@login_required
def delete_document_reminder(request, pk):
    """Utility Feature B: Delete Document Reminder."""
    reminder = get_object_or_404(DocumentReminder, pk=pk, user=request.user)
    reminder.delete()
    messages.success(request, "Document reminder removed.")
    return redirect('booking_history')

def multi_destination_explorer(request):
    """
    Utility Feature C: Multi-Destination Travel Explorer
    Select multiple Kerala spots, plan routes, calculate travel distance, time, and budget.
    """
    all_dests = ['Alappuzha', 'Athirappilly', 'Munnar', 'Thekkady', 'Wayanad', 'Palakkad', 'Varkala', 'Kozhikode', 'Bekal']
    selected = request.GET.getlist('stops') or ['Alappuzha', 'Munnar', 'Thekkady']

    route_data = calculate_route_matrix(selected)

    return render(
        request,
        'bookings/multi_destination.html',
        {
            'all_destinations': all_dests,
            'selected_destinations': selected,
            'route_data': route_data,
        }
    )

def nearby_places(request):
    """
    Utility Feature A: Nearby Places Finder
    Restaurants, hospitals, pharmacies, ATMs, and emergency services for Kerala destinations.
    """
    dest_name = request.GET.get('dest', 'Munnar')
    place_type = request.GET.get('type', 'all')

    services_data = {
        'Munnar': [
            {'name': 'Devikulam Primary Health Centre', 'type': 'Hospital', 'distance': '3.8 km', 'contact': '+91 4865 264225', 'rating': '4.6'},
            {'name': 'RDR Speciality Pharmacy', 'type': 'Pharmacy', 'distance': '1.2 km', 'contact': '+91 4865 230412', 'rating': '4.5'},
            {'name': 'SBI ATM & Cash Deposit', 'type': 'ATM', 'distance': '0.8 km', 'contact': '24/7 Available', 'rating': '4.2'},
            {'name': 'Rapsy Restaurant (Kerala Parotta & Beef)', 'type': 'Restaurant', 'distance': '1.5 km', 'contact': '+91 4865 230456', 'rating': '4.8'},
            {'name': 'Munnar Tourist Police Station', 'type': 'Emergency', 'distance': '2.1 km', 'contact': '112 / +91 4865 230321', 'rating': '4.9'},
        ],
        'Alappuzha': [
            {'name': 'Alappuzha General Hospital', 'type': 'Hospital', 'distance': '2.5 km', 'contact': '+91 477 2253324', 'rating': '4.5'},
            {'name': 'Apollo Pharmacy Boat Jetty Road', 'type': 'Pharmacy', 'distance': '0.5 km', 'contact': '+91 477 2261234', 'rating': '4.6'},
            {'name': 'HDFC Bank ATM Canal Road', 'type': 'ATM', 'distance': '0.4 km', 'contact': '24/7 Available', 'rating': '4.4'},
            {'name': 'Thaff Restaurant (Biryani & Seafood)', 'type': 'Restaurant', 'distance': '1.1 km', 'contact': '+91 477 2235612', 'rating': '4.7'},
            {'name': 'Alappuzha Coastal Police Station', 'type': 'Emergency', 'distance': '1.8 km', 'contact': '112 / +91 477 2251234', 'rating': '4.8'},
        ],
        'Wayanad': [
            {'name': 'Wayanad District Hospital Mananthavady', 'type': 'Hospital', 'distance': '5.2 km', 'contact': '+91 4935 240223', 'rating': '4.6'},
            {'name': 'CareWell Meds Sulthan Bathery', 'type': 'Pharmacy', 'distance': '1.0 km', 'contact': '+91 4936 220199', 'rating': '4.4'},
            {'name': 'Canara Bank ATM Kalpetta', 'type': 'ATM', 'distance': '0.6 km', 'contact': '24/7 Available', 'rating': '4.3'},
            {'name': '1980s A Nostalgic Restaurant', 'type': 'Restaurant', 'distance': '2.4 km', 'contact': '+91 4936 206180', 'rating': '4.9'},
            {'name': 'Kalpetta Tourist Police Helpline', 'type': 'Emergency', 'distance': '1.3 km', 'contact': '112 / +91 4936 202233', 'rating': '4.8'},
        ]
    }

    selected_services = services_data.get(dest_name, services_data['Munnar'])
    if place_type != 'all':
        selected_services = [s for s in selected_services if s['type'].lower() == place_type.lower()]

    all_dests = ['Munnar', 'Alappuzha', 'Wayanad']

    return render(
        request,
        'bookings/nearby_places.html',
        {
            'services': selected_services,
            'selected_dest': dest_name,
            'selected_type': place_type,
            'all_dests': all_dests,
        }
    )
