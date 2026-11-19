from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from .models import TravelPreference, UserProfile, Notification
from destinations.models import Destination, Wishlist
from bookings.models import Booking
from recomendations.ml_engine import recommend_destinations

def user_logout(request):
    """Handle logout via both GET and POST without HTTP 405 error."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
            # Create welcome notification
            Notification.objects.create(
                user=user,
                title="Welcome to TravelMate AI!",
                message="Your intelligent travel companion for Kerala is ready. Explore curated destinations and plan your next journey.",
                notification_type="system",
                link="/destinations/"
            )
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to TravelMate AI.')
            return redirect('user_dashboard')
    else:
        form = CustomUserCreationForm()

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
    AI Recommended destinations, 'Ask TravelMate AI' interactive widget,
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
        upcoming_booking = Booking.objects.order_by('-created_at').first()

    featured_destinations = Destination.objects.filter(is_hidden_gem=False).order_by('-popularity_score')[:4]

    # Get ML Recommendations for the user
    ai_recommendations = recommend_destinations(
        user_interests=preference.interests,
        preferred_climate=preference.preferred_climate,
        budget=preference.budget,
        preferred_category=preference.preferred_category,
        top_n=3
    )

    # Calculate expense pool percentage
    limit = profile.budget_limit or 25000.0
    spent = profile.total_spent or 14200.0
    spent_pct = int(min(100, (spent / limit) * 100))

    # Unread notifications
    unread_notifs = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(
        request,
        'user/dashboard.html',
        {
            'profile': profile,
            'preference': preference,
            'upcoming_booking': upcoming_booking,
            'featured_destinations': featured_destinations,
            'ai_recommendations': ai_recommendations,
            'spent_pct': spent_pct,
            'spent': spent,
            'limit': limit,
            'unread_notifs': unread_notifs,
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

@login_required
def toggle_wishlist(request, dest_id):
    """AJAX / Form endpoint to add or remove a destination from wishlist."""
    destination = get_object_or_404(Destination, pk=dest_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, destination=destination)

    if not created:
        item.delete()
        is_wishlisted = False
        msg = f"Removed {destination.name} from your wishlist."
    else:
        is_wishlisted = True
        msg = f"Saved {destination.name} to your wishlist!"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({'status': 'success', 'is_wishlisted': is_wishlisted, 'message': msg})

    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'destination_list'))

@login_required
def wishlist(request):
    """View all destinations saved to user wishlist."""
    items = Wishlist.objects.filter(user=request.user).select_related('destination')
    return render(request, 'user/wishlist.html', {'wishlist_items': items})

@login_required
def travel_history(request):
    """View completed bookings and historical travel logs."""
    history = Booking.objects.filter(user=request.user, status__in=['Completed', 'Confirmed']).order_by('-travel_date')
    return render(request, 'user/travel_history.html', {'history': history})

@login_required
def notifications_view(request):
    """View all system and booking notifications."""
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    # Mark as read
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'user/notifications.html', {'notifications': notifs})
