from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TravelPreference, UserProfile
from destinations.models import Destination
from bookings.models import Booking

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Initialize profile and preferences
            UserProfile.objects.create(
                user=user,
                phone='',
                bio='New traveller on TravelMate AI'
            )
            TravelPreference.objects.create(
                user=user,
                interests='Nature, Trekking',
                preferred_climate='Cool',
                budget=15000.0,
                preferred_category='Hill Station'
            )
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to TravelMate AI.')
            return redirect('user_dashboard')
    else:
        form = UserCreationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

@login_required
def user_dashboard(request):
    """
    Figma Screen 1: Traveller Dashboard
    Upcoming trip tracker, Expense Pool meter, Smart shortcuts,
    Featured destinations, 'Ask TravelMate AI' interactive widget,
    and active Booking voucher with QR code.
    """
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'total_spent': 14200.0, 'budget_limit': 25000.0}
    )
    preference, _ = TravelPreference.objects.get_or_create(
        user=request.user,
        defaults={'interests': 'Nature, High Altitude Trekking', 'preferred_climate': 'Cool', 'budget': 15000.0, 'preferred_category': 'Hill Station'}
    )

    # Active upcoming booking
    upcoming_booking = Booking.objects.filter(user=request.user).order_by('-created_at').first()
    if not upcoming_booking:
        # Fallback to any recent booking for showcase
        upcoming_booking = Booking.objects.order_by('-created_at').first()

    featured_destinations = Destination.objects.filter(is_hidden_gem=False).order_by('-popularity_score')[:4]

    # Calculate expense pool percentage
    limit = profile.budget_limit or 25000.0
    spent = profile.total_spent or 14200.0
    spent_pct = int(min(100, (spent / limit) * 100))

    return render(
        request,
        'user/dashboard.html',
        {
            'profile': profile,
            'preference': preference,
            'upcoming_booking': upcoming_booking,
            'featured_destinations': featured_destinations,
            'spent_pct': spent_pct,
            'spent': spent,
            'limit': limit,
        }
    )

@login_required
def preferences(request):
    preference, created = TravelPreference.objects.get_or_create(
        user=request.user,
        defaults={
            'interests': 'Nature, Scenic Views, Trekking',
            'preferred_climate': 'Cool',
            'budget': 15000.0,
            'preferred_category': 'Hill Station',
            'travel_style': 'Solo Explorer'
        }
    )

    if request.method == 'POST':
        preference.interests = request.POST.get('interests', '')
        preference.preferred_climate = request.POST.get('climate', 'Cool')
        preference.budget = float(request.POST.get('budget', 15000.0))
        preference.preferred_category = request.POST.get('category', 'Hill Station')
        preference.travel_style = request.POST.get('travel_style', 'Solo Explorer')
        preference.save()

        messages.success(request, 'Travel preferences updated! AI recommendations refreshed.')
        return redirect('user_dashboard')

    return render(
        request,
        'user/preferences.html',
        {'preference': preference}
    )
