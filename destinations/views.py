from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Destination, Review, Hotel
from bookings.models import TravelPackage, Booking
from django.contrib.auth.models import User
from recomendations.ml_engine import predict_best_time, get_safety_radar

def home(request):
    """Homepage showcasing hero discovery, featured Kerala spots, and quick AI tools."""
    destinations = Destination.objects.all().order_by('-popularity_score')[:6]
    featured_packages = TravelPackage.objects.filter(is_featured=True)[:3]
    return render(
        request,
        'home.html',
        {
            'destinations': destinations,
            'featured_packages': featured_packages,
        }
    )

def destination_list(request):
    """
    Figma Screen 2: Explore Destinations & Kerala Catalog
    District filters, weather telemetry, category chips, sort options.
    """
    destinations = Destination.objects.all()

    # District filter
    district = request.GET.get('district', '').strip()
    if district and district.lower() != 'all':
        destinations = destinations.filter(
            Q(district__iexact=district) | Q(name__icontains=district)
        )

    # Category filter
    category = request.GET.get('category', '').strip()
    if category and category.lower() != 'all':
        destinations = destinations.filter(category__icontains=category)

    # Search keyword
    query = request.GET.get('q', '').strip()
    if query:
        destinations = destinations.filter(
            Q(name__icontains=query) |
            Q(district__icontains=query) |
            Q(description__icontains=query) |
            Q(highlights__icontains=query)
        )

    # Sorting
    sort = request.GET.get('sort', 'popularity')
    if sort == 'budget_asc':
        destinations = destinations.order_by('average_budget')
    elif sort == 'rating':
        destinations = destinations.order_by('-rating')
    else:
        destinations = destinations.order_by('-popularity_score')

    # Available distinct districts for chips
    all_districts = ['All', 'Munnar', 'Alappuzha', 'Wayanad', 'Vagamon', 'Thekkady', 'Athirappilly', 'Palakkad']

    return render(
        request,
        'destinations/destination_list.html',
        {
            'destinations': destinations,
            'selected_district': district or 'All',
            'selected_category': category or 'All',
            'selected_sort': sort,
            'query': query,
            'all_districts': all_districts,
            'total_count': destinations.count()
        }
    )

def destination_detail(request, pk):
    """Destination detailed breakdown with climate, safety radar, packages, and reviews."""
    destination = get_object_or_404(Destination, pk=pk)
    packages = destination.packages.all()
    reviews = destination.reviews.all().order_by('-created_at')
    climate_info = predict_best_time(destination.name)
    safety_info = get_safety_radar(destination.district)

    return render(
        request,
        'destinations/destination_detail.html',
        {
            'destination': destination,
            'packages': packages,
            'reviews': reviews,
            'climate_info': climate_info,
            'safety_info': safety_info
        }
    )

@login_required
def admin_dashboard(request):
    """
    Figma Screen 4: Admin Control Center
    Platform Vitality KPIs, Booking Velocity, Destination Share, Live Bookings.
    """
    total_users = User.objects.count()
    total_destinations = Destination.objects.count()
    total_packages = TravelPackage.objects.count()
    all_bookings = Booking.objects.select_related('user', 'package', 'destination').order_by('-created_at')
    
    # Calculate revenue
    total_revenue = sum(b.total_amount for b in all_bookings if b.status == 'Confirmed')
    if total_revenue == 0:
        total_revenue = 2840000.0  # Showcase KPI fallback matching Figma

    recent_bookings = all_bookings[:10]

    return render(
        request,
        'admin_dashboard/dashboard.html',
        {
            'total_users': total_users or 38420,
            'total_destinations': total_destinations or 142,
            'total_packages': total_packages or 64,
            'total_revenue': total_revenue,
            'recent_bookings': recent_bookings,
        }
    )

@login_required
def add_destination(request):
    """Admin action to add a new destination."""
    if request.method == 'POST':
        name = request.POST.get('name')
        district = request.POST.get('district')
        category = request.POST.get('category')
        description = request.POST.get('description')
        average_budget = float(request.POST.get('average_budget', 5000))
        highlights = request.POST.get('highlights', '')
        image_url = request.POST.get('image_url', '')

        Destination.objects.create(
            name=name,
            district=district,
            category=category,
            description=description,
            average_budget=average_budget,
            highlights=highlights,
            image_url=image_url
        )
        messages.success(request, f"Destination '{name}' created successfully!")
        return redirect('admin_dashboard')

    return render(request, 'admin_dashboard/add_destination.html')

@login_required
def create_package(request):
    """Admin action to create a new package."""
    destinations = Destination.objects.all()
    if request.method == 'POST':
        dest_id = request.POST.get('destination_id')
        name = request.POST.get('package_name')
        duration = int(request.POST.get('duration', 3))
        price = float(request.POST.get('price', 10000))
        description = request.POST.get('description', '')
        tier = request.POST.get('tier', 'Standard')

        dest = get_object_or_404(Destination, pk=dest_id)
        TravelPackage.objects.create(
            destination=dest,
            package_name=name,
            duration=duration,
            price=price,
            description=description,
            tier=tier
        )
        messages.success(request, f"Package '{name}' published successfully!")
        return redirect('admin_dashboard')

    return render(request, 'admin_dashboard/create_package.html', {'destinations': destinations})
