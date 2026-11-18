from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.models import TravelPreference
from destinations.models import Destination
from .models import TravelBuddy, SavedItinerary
from .ml_engine import (
    recommend_destinations,
    predict_best_time,
    get_hidden_gems,
    match_travel_buddies,
    analyze_review_sentiment,
    optimize_travel_cost,
    get_outfit_recommendations,
    get_malayalam_translations,
    calculate_carbon_footprint,
    get_safety_radar,
    calculate_route_matrix,
    generate_ai_trip_plan,
)

def assistant_hub(request):
    """
    Figma Screen 3: AI Travel Intelligence Hub
    Interactive showcase of all 11 AI & ML tools with real-time outputs.
    """
    # Active tab from query param
    active_tab = request.GET.get('tab', 'all')

    # Get user preferences if authenticated
    if request.user.is_authenticated:
        pref, _ = TravelPreference.objects.get_or_create(
            user=request.user,
            defaults={'interests': 'Nature, High Altitude Trekking', 'preferred_climate': 'Cool', 'budget': 15000.0, 'preferred_category': 'Hill Station'}
        )
        user_interests = pref.interests
        preferred_climate = pref.preferred_climate
        budget = pref.budget
        preferred_category = pref.preferred_category
    else:
        user_interests = 'Nature, High Altitude Trekking, Tea Trails'
        preferred_climate = 'Cool'
        budget = 15000.0
        preferred_category = 'Hill Station'

    # Tool 1: ML Destination Recommender
    recommendations = recommend_destinations(user_interests, preferred_climate, budget, preferred_category)

    # Tool 2 & Spotlight: AI Trip Planner / 48-Hour Generator
    selected_dest = request.GET.get('dest', 'Munnar')
    itinerary = generate_ai_trip_plan(selected_dest, days=3, budget=budget)

    # Tool 3: Best Time to Visit Predictor
    climate_info = predict_best_time(selected_dest)

    # Tool 4: Hidden Gems
    hidden_gems = get_hidden_gems()

    # Tool 5: Travel Buddy Matching
    buddies = match_travel_buddies(user_interests, selected_dest)

    # Tool 6: Review Sentiment Analyzer (Sample or user submitted)
    sample_review = request.GET.get('review_text', "Kolukkumalai sunrise and pristine tea gardens were an incredible experience. Homestay food was delicious and hosts were hospitable!")
    sentiment = analyze_review_sentiment(sample_review)

    # Tool 7: AI Cost Optimizer
    cost_optimization = optimize_travel_cost(package_price=18400.0, days=4)

    # Tool 8: AI Outfit & Packing Stylist
    outfits = get_outfit_recommendations(selected_dest)

    # Tool 9: Malayalam Dialect Voice AI
    translations = get_malayalam_translations()

    # Tool 10: Sustainable Travel Footprint
    carbon = calculate_carbon_footprint(days=4)

    # Tool 11: Safety Score Radar
    safety = get_safety_radar(selected_dest)

    # Bonus: Multi-Destination Route Matrix
    route = calculate_route_matrix(['Alappuzha', 'Athirappilly', 'Munnar', 'Thekkady'])

    all_destinations = Destination.objects.all()

    return render(
        request,
        'recomendations/assistant_hub.html',
        {
            'active_tab': active_tab,
            'selected_dest': selected_dest,
            'all_destinations': all_destinations,
            'recommendations': recommendations,
            'itinerary': itinerary,
            'climate_info': climate_info,
            'hidden_gems': hidden_gems,
            'buddies': buddies,
            'sample_review': sample_review,
            'sentiment': sentiment,
            'cost_optimization': cost_optimization,
            'outfits': outfits,
            'translations': translations,
            'carbon': carbon,
            'safety': safety,
            'route': route,
            'user_interests': user_interests,
            'preferred_climate': preferred_climate,
            'budget': budget,
            'preferred_category': preferred_category,
        }
    )

@csrf_exempt
def ask_ai(request):
    """
    API endpoint for interactive 'Ask TravelMate AI' conversational widget
    answering route questions, packing checklists, and local recommendations.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').strip()
        except Exception:
            query = request.POST.get('query', '').strip()

        if not query:
            return JsonResponse({'response': "Please enter a travel question! For example: 'What to pack for Munnar trek?'"})

        q_lower = query.lower()

        if 'pack' in q_lower or 'clothes' in q_lower or 'outfit' in q_lower:
            reply = (
                "🧥 **Munnar Packing Recommendations:**\n"
                "• Mornings & Nights (14°C): Windproof fleece jacket or thermal layer.\n"
                "• Day Trekking: Breathable dry-fit shirts & cargo pants.\n"
                "• Footwear: Grip trail sneakers with mud traction.\n"
                "• Add-ons: Rain poncho, leech socks (for forest trails), and UV sunglasses."
            )
        elif 'homestay' in q_lower or 'stay' in q_lower or 'hotel' in q_lower:
            reply = (
                "🏡 **Top Quiet Estate Homestays:**\n"
                "1. **Cloud Valley Plantation Retreat (Tea Valley Road):** Heritage bungalow nestled inside working organic tea terraces.\n"
                "2. **Misty Windmills Eco-Camp:** Secluded solar-powered cottages with valley panoramas.\n"
                "3. **Periyar Spice Haven:** Homestay surrounded by cinnamon and pepper vines."
            )
        elif 'fish' in q_lower or 'food' in q_lower or 'restaurant' in q_lower:
            reply = (
                "🍲 **Authentic Kerala Culinary Highlights:**\n"
                "• Must try: Fresh Pearl Spot (Karimeen Pollichathu) baked in banana leaves.\n"
                "• En route stops: Wayside Toddy Shop style fish curry meals along Cochin-Munnar NH85.\n"
                "• Local phrase to remember: *'Kaaram kuravu mathi'* (Make it less spicy)."
            )
        elif 'safe' in q_lower or 'weather' in q_lower:
            reply = (
                "🛡️ **Current Safety & Route Status:**\n"
                "• High-Range Zone: Low landslide hazard. NH85 Gap Road is completely clear.\n"
                "• Night travel is safe with fog lamps until 10:00 PM.\n"
                "• Emergency helpline: Toll-free **112** (Active 24/7 across Idukki & Ernakulam)."
            )
        else:
            reply = (
                f"✨ **TravelMate AI Advice for '{query}':**\n"
                "We recommend pairing morning visits (06:00 AM - 10:30 AM) for mist-free visibility, "
                "booking Kerala Forest Department permits in advance for Eravikulam & Chembra Peak, "
                "and utilizing KSRTC Low-floor AC transit to save up to 32% on route costs."
            )

        return JsonResponse({'status': 'success', 'query': query, 'response': reply})

    return JsonResponse({'error': 'POST request required'}, status=400)

@csrf_exempt
def sentiment_api(request):
    """API for dynamic testing of review sentiment."""
    text = request.POST.get('review_text', '')
    res = analyze_review_sentiment(text)
    return JsonResponse(res)
