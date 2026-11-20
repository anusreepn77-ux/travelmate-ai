from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
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
    preference, _ = TravelPreference.objects.get_or_create(
        user=request.user,
        defaults={'interests': 'Nature, High Altitude Trekking', 'preferred_climate': 'Cool', 'budget': 15000.0, 'preferred_category': 'Hill Station'}
    )

    upcoming_booking = (
        Booking.objects.filter(
            user=request.user,
            status__in=['Confirmed', 'Pending'],
            travel_date__gte=timezone.localdate(),
        )
        .select_related('package', 'destination', 'package__destination')
        .order_by('travel_date', '-created_at')
        .first()
    )

    all_destinations = []
    seen_destinations = set()
    for destination in Destination.objects.order_by('-popularity_score', 'name'):
        identity = (destination.name.strip().casefold(), destination.district.strip().casefold())
        if identity not in seen_destinations:
            seen_destinations.add(identity)
            all_destinations.append(destination)

    total_destinations = len(all_destinations)
    featured_destinations = [
        destination for destination in all_destinations
        if not destination.is_hidden_gem
    ][:4]
    featured_keys = {
        (destination.name.strip().casefold(), destination.district.strip().casefold())
        for destination in featured_destinations
    }

    # Get ML Recommendations for the user
    recommended_destinations = recommend_destinations(
        user_interests=preference.interests,
        preferred_climate=preference.preferred_climate,
        budget=preference.budget,
        preferred_category=preference.preferred_category,
        top_n=3
    )
    ai_recommendations = []
    seen_recommendations = set(featured_keys)
    for recommendation in recommended_destinations:
        destination = recommendation['destination']
        identity = (destination.name.strip().casefold(), destination.district.strip().casefold())
        if identity not in seen_recommendations:
            seen_recommendations.add(identity)
            ai_recommendations.append(recommendation)

    limit = preference.budget
    booked_total = (
        Booking.objects.filter(
            user=request.user,
            status__in=['Confirmed', 'Completed'],
        ).aggregate(total=Sum('total_amount'))['total']
        or 0
    )
    spent_pct = int(min(100, (booked_total / limit) * 100)) if limit > 0 else 0
    safe_margin = max(limit - booked_total, 0)

    # Unread notifications
    unread_notifs = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(
        request,
        'user/dashboard.html',
        {
            'preference': preference,
            'upcoming_booking': upcoming_booking,
            'featured_destinations': featured_destinations,
            'total_destinations': total_destinations,
            'ai_recommendations': ai_recommendations,
            'spent_pct': spent_pct,
            'booked_total': booked_total,
            'limit': limit,
            'safe_margin': safe_margin,
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
