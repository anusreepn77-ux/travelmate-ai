import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelmateai.settings')
django.setup()

from django.contrib.auth.models import User
from destinations.models import Destination, Review, Hotel
from bookings.models import TravelPackage, Booking, DocumentReminder
from accounts.models import TravelPreference, UserProfile
from recomendations.models import TravelBuddy

def seed():
    print("Seeding TravelMate AI database...")

    # 1. Admin & Test User Setup
    admin_user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@travelmate.ai'})
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.first_name = "Rahul"
    admin_user.last_name = "Sharma"
    admin_user.save()

    UserProfile.objects.update_or_create(
        user=admin_user,
        defaults={
            'phone': '+91 98470 12345',
            'bio': 'Outdoor enthusiast exploring Kerala high ranges and backwaters.',
            'avatar_url': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
            'total_spent': 14200.0,
            'budget_limit': 25000.0,
        }
    )

    TravelPreference.objects.update_or_create(
        user=admin_user,
        defaults={
            'interests': 'Nature, High Altitude Trekking, Tea Trails, Photography',
            'preferred_climate': 'Cool',
            'budget': 15000.0,
            'preferred_category': 'Hill Station',
            'travel_style': 'Solo Explorer'
        }
    )

    # 2. Kerala Destinations (matching PDF + Figma)
    destinations_data = [
        {
            'name': 'Munnar',
            'district': 'Idukki',
            'category': 'Hill Station',
            'description': 'Endless tea gardens, misty peaks, cool highland climate, and home of the endangered Nilgiri Tahr.',
            'average_budget': 8500.0,
            'best_month': 'October to May',
            'popularity_score': 94,
            'climate': 'Cool & Misty (15-22°C)',
            'image_url': 'https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80',
            'is_hidden_gem': False,
            'highlights': 'Eravikulam National Park, Mattupetty Dam, Tea Museum, Anamudi Peak',
            'rating': 4.8,
            'reviews_count': 2400,
            'estimated_days': 3,
            'eco_friendly': True,
            'eco_tags': 'Certified Organic Tea, Zero-Plastic Homestays, Solar Energy',
            'safety_score': 96,
            'crowd_density': 'High'
        },
        {
            'name': 'Alappuzha',
            'district': 'Alappuzha',
            'category': 'Backwaters',
            'description': 'The Venice of the East, famous for serene palm-fringed canals, luxury houseboats, and coir heritage.',
            'average_budget': 11000.0,
            'best_month': 'November to February',
            'popularity_score': 92,
            'climate': 'Tropical & Coastal (24-30°C)',
            'image_url': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80',
            'is_hidden_gem': False,
            'highlights': 'Vembanad Houseboat Cruise, Marari Beach, Pathiramanal Island, Kuttanad Paddy Fields',
            'rating': 4.9,
            'reviews_count': 3100,
            'estimated_days': 2,
            'eco_friendly': True,
            'eco_tags': 'Solar Powered Electric Boats, Farm-to-Table Kerala Meals',
            'safety_score': 94,
            'crowd_density': 'High'
        },
        {
            'name': 'Wayanad',
            'district': 'Wayanad',
            'category': 'Mountain & Nature',
            'description': 'Pristine rainforests, spice plantations, prehistoric caves, and rolling mountain ridges in the Western Ghats.',
            'average_budget': 7200.0,
            'best_month': 'September to May',
            'popularity_score': 89,
            'climate': 'Pleasant & Cool (18-26°C)',
            'image_url': 'https://images.unsplash.com/photo-1588661750275-d147bbfa99b4?auto=format&fit=crop&w=800&q=80',
            'is_hidden_gem': False,
            'highlights': 'Banasura Sagar Dam, Chembra Peak Heart Lake, Edakkal Caves, Muthanga Wildlife',
            'rating': 4.7,
            'reviews_count': 1800,
            'estimated_days': 3,
            'eco_friendly': True,
            'eco_tags': 'Tribal Community Tourism, Rainforest Conservation, Bamboo Stays',
            'safety_score': 92,
            'crowd_density': 'Moderate'
        },
        {
            'name': 'Vagamon',
            'district': 'Idukki',
            'category': 'Hill Station',
            'description': 'An idyllic offbeat hill station with velvet green rolling meadows, pine forest groves, and tea plantations.',
            'average_budget': 5500.0,
            'best_month': 'Throughout the year',
            'popularity_score': 76,
            'climate': 'Cool Breeze (16-24°C)',
            'image_url': 'https://images.unsplash.com/photo-1629853926838-8c1d3c01c0c5?auto=format&fit=crop&w=800&q=80',
            'is_hidden_gem': True,
            'highlights': 'Vagamon Pine Forest, Kurisumala Ashram, Green Meadows, Paragliding Point',
            'rating': 4.6,
            'reviews_count': 920,
            'estimated_days': 2,
            'eco_friendly': True,
            'eco_tags': 'Low Commercialization, Off-Grid Eco Camps, Waste-Free Trails',
            'safety_score': 95,
            'crowd_density': 'Low'
        },
        {
            'name': 'Thekkady',
            'district': 'Idukki',
            'category': 'Wildlife Sanctuary',
            'description': 'Periyar National Park sanctuary with wild elephants, aromatic spice plantations, and bamboo rafting.',
            'average_budget': 9000.0,
            'best_month': 'October to March',
            'popularity_score': 91,
            'climate': 'Temperate Forest (19-27°C)',
            'image_url': 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80',
            'is_hidden_gem': False,
            'highlights': 'Periyar Lake Boat Safari, Spice Garden Walk, Bamboo Rafting, Elephant Junction',
            'rating': 4.8,
            'reviews_count': 1900,
            'estimated_days': 3,
            'eco_friendly': True,
            'eco_tags': 'Forest Department Guided Patrols, Plastic Ban Zone',
            'safety_score': 93,
            'crowd_density': 'Moderate'
        },
        {
            'name': 'Athirappilly',
            'district': 'Thrissur',
            'category': 'Waterfalls & Forest',
            'description': 'The Niagara of India, a magnificent 80-foot wide waterfall cascading through lush Sholayar rainforest.',
            'average_budget': 4500.0,
            'best_month': 'June to January (Post Monsoon)',
            'popularity_score': 78,
            'climate': 'Humid Tropical (22-29°C)',
            'image_url': 'https://images.unsplash.com/photo-1546548970-71785318a17b?auto=format&fit=crop&w=800&q=80',
            'is_hidden_gem': False,
            'highlights': 'Athirappilly Falls, Vazhachal Cascade, Rainforest Viewpoint, Chapra Falls',
            'rating': 4.7,
            'reviews_count': 1400,
            'estimated_days': 1,
            'eco_friendly': True,
            'eco_tags': 'Kadar Tribe Eco-Tours, River Basin Conservation',
            'safety_score': 90,
            'crowd_density': 'Moderate'
        },
        {
            'name': 'Palakkad',
            'district': 'Palakkad',
            'category': 'Heritage & Valley',
            'description': 'The Granary of Kerala, marked by the Palakkad Gap in the Western Ghats, historic granite fort, and Silent Valley.',
            'average_budget': 4800.0,
            'best_month': 'November to February',
            'popularity_score': 75,
            'climate': 'Warm & Breezy (21-31°C)',
            'image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
            'is_hidden_gem': False,
            'highlights': 'Malampuzha Dam, Nelliyampathy Hills, Silent Valley Rainforest, Dhoni Waterfalls',
            'rating': 4.6,
            'reviews_count': 850,
            'estimated_days': 2,
            'eco_friendly': True,
            'eco_tags': 'Silent Valley Buffer Zone Protection, Agro-Tourism',
            'safety_score': 95,
            'crowd_density': 'Low'
        },
        {
            'name': 'Marari Beach',
            'district': 'Alappuzha',
            'category': 'Beach & Coastal',
            'description': 'Secluded golden sand beach bordered by endless coconut groves, traditional fishing catamarans, and peace.',
            'average_budget': 6500.0,
            'best_month': 'October to March',
            'popularity_score': 71,
            'climate': 'Sea Breeze Tropical (25-31°C)',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
            'is_hidden_gem': True,
            'highlights': 'Marari Beachfront, Traditional Coir Making, Sea Turtle Hatchery, Ayurvedic Centers',
            'rating': 4.7,
            'reviews_count': 950,
            'estimated_days': 2,
            'eco_friendly': True,
            'eco_tags': 'No Jet-skis Policy, Community Beach Conservation',
            'safety_score': 97,
            'crowd_density': 'Low'
        },
        {
            'name': 'Nelliyampathy',
            'district': 'Palakkad',
            'category': 'Hill Station',
            'description': 'Misty cloud-capped heights surrounded by private tea and bio-farm cardamom estates with breathtaking drop-offs.',
            'average_budget': 5200.0,
            'best_month': 'September to May',
            'popularity_score': 68,
            'climate': 'Misty & Chill (15-21°C)',
            'image_url': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80',
            'is_hidden_gem': True,
            'highlights': 'Kesavampara View, Seethargundu 1000m Drop, Organic Orange Orchards, Pothundi Reservoir',
            'rating': 4.6,
            'reviews_count': 620,
            'estimated_days': 2,
            'eco_friendly': True,
            'eco_tags': 'Certified Organic Bio-Farms, Low Carbon Footprint',
            'safety_score': 93,
            'crowd_density': 'Low'
        }
    ]

    dest_objs = {}
    for data in destinations_data:
        dest, _ = Destination.objects.update_or_create(name=data['name'], defaults=data)
        dest_objs[dest.name] = dest

    # 3. Travel Packages (matching PDF + Figma)
    packages_data = [
        {
            'destination': dest_objs['Munnar'],
            'package_name': 'Munnar & Tea Hills Trek',
            'duration': 4,
            'duration_nights': 3,
            'price': 18400.0,
            'tier': 'Luxury',
            'is_featured': True,
            'description': 'Full high-altitude tea estate immersion including Kolukkumalai sunrise safari, Eravikulam alpine track, and Pothamedu sunset photography.',
            'image_url': 'https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80'
        },
        {
            'destination': dest_objs['Alappuzha'],
            'package_name': 'Alappuzha Premium Houseboat Cruise',
            'duration': 3,
            'duration_nights': 2,
            'price': 22000.0,
            'tier': 'Luxury',
            'is_featured': True,
            'description': 'Private luxury wooden houseboat cruising Vembanad backwaters with personal chef, fresh Karimeen fry, and sunset canoe excursion.',
            'image_url': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80'
        },
        {
            'destination': dest_objs['Wayanad'],
            'package_name': 'Wayanad Rainforest & Wildlife Camp',
            'duration': 3,
            'duration_nights': 2,
            'price': 12400.0,
            'tier': 'Eco',
            'is_featured': True,
            'description': 'Stay in elevated bamboo huts, trek Chembra heart lake, and embark on an open jeep safari through Muthanga sanctuary.',
            'image_url': 'https://images.unsplash.com/photo-1588661750275-d147bbfa99b4?auto=format&fit=crop&w=800&q=80'
        },
        {
            'destination': dest_objs['Vagamon'],
            'package_name': 'Vagamon Offbeat Pine Trail & Paragliding',
            'duration': 3,
            'duration_nights': 2,
            'price': 9800.0,
            'tier': 'Eco',
            'is_featured': False,
            'description': 'Quiet pine forest trails, Kurisumala monastery trek, and tandem paragliding over rolling green meadows.',
            'image_url': 'https://images.unsplash.com/photo-1629853926838-8c1d3c01c0c5?auto=format&fit=crop&w=800&q=80'
        },
        {
            'destination': dest_objs['Athirappilly'],
            'package_name': 'Athirappilly & Vazhachal Cascade Explorer',
            'duration': 2,
            'duration_nights': 1,
            'price': 7500.0,
            'tier': 'Standard',
            'is_featured': False,
            'description': 'Witness majestic waterfalls cascading through rainforest, riverbank hiking, and local tribal cultural lunch.',
            'image_url': 'https://images.unsplash.com/photo-1546548970-71785318a17b?auto=format&fit=crop&w=800&q=80'
        }
    ]

    pkg_objs = {}
    for pdata in packages_data:
        pkg, _ = TravelPackage.objects.update_or_create(package_name=pdata['package_name'], defaults=pdata)
        pkg_objs[pkg.package_name] = pkg

    # 4. Bookings (matching Figma Screen 1 & Screen 4)
    import datetime
    today = datetime.date.today()
    
    # Active booking for admin/Rahul
    Booking.objects.update_or_create(
        user=admin_user,
        package=pkg_objs['Munnar & Tea Hills Trek'],
        defaults={
            'destination': dest_objs['Munnar'],
            'travel_date': today + datetime.timedelta(days=4),
            'number_of_people': 2,
            'total_amount': 18400.0,
            'status': 'Confirmed',
            'voucher_code': 'TM-99412'
        }
    )

    # Secondary users for admin dashboard
    user2, _ = User.objects.get_or_create(username='ananya_patel', defaults={'email': 'ananya@gmail.com', 'first_name': 'Ananya', 'last_name': 'Patel'})
    Booking.objects.update_or_create(
        user=user2,
        package=pkg_objs['Alappuzha Premium Houseboat Cruise'],
        defaults={
            'destination': dest_objs['Alappuzha'],
            'travel_date': today + datetime.timedelta(days=12),
            'number_of_people': 2,
            'total_amount': 22000.0,
            'status': 'Confirmed',
            'voucher_code': 'TM-84310'
        }
    )

    user3, _ = User.objects.get_or_create(username='david_miller', defaults={'email': 'david@gmail.com', 'first_name': 'David', 'last_name': 'Miller'})
    Booking.objects.update_or_create(
        user=user3,
        package=pkg_objs['Wayanad Rainforest & Wildlife Camp'],
        defaults={
            'destination': dest_objs['Wayanad'],
            'travel_date': today + datetime.timedelta(days=20),
            'number_of_people': 1,
            'total_amount': 12400.0,
            'status': 'Pending',
            'voucher_code': 'TM-77291'
        }
    )

    # 5. Travel Buddies (matching Figma Screen 3)
    buddies_data = [
        {
            'name': 'Adari H.',
            'destination': dest_objs['Wayanad'],
            'travel_dates': 'Oct 24 - Oct 28',
            'interests': 'Wayanad Peak Trekking, Mountain Biking, Sunrise Photography',
            'compatibility_score': 94.0,
            'trips_completed': 6,
            'bio': 'Solo backpacker who loves early morning peak photography and local food.',
            'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80'
        },
        {
            'name': 'Kavya M.',
            'destination': dest_objs['Munnar'],
            'travel_dates': 'Nov 02 - Nov 06',
            'interests': 'Tea Plantation Walks, Birdwatching, Slow Travel, Sketching',
            'compatibility_score': 91.0,
            'trips_completed': 4,
            'bio': 'Architect exploring colonial tea estate bungalows and endemic flora.',
            'avatar_url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80'
        },
        {
            'name': 'Rohan K.',
            'destination': dest_objs['Alappuzha'],
            'travel_dates': 'Nov 10 - Nov 14',
            'interests': 'Kayaking, Local Seafood Trails, Houseboat Co-living',
            'compatibility_score': 88.0,
            'trips_completed': 5,
            'bio': 'Remote software engineer seeking reliable Wi-Fi homestays in backwaters.',
            'avatar_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80'
        }
    ]

    for bdata in buddies_data:
        TravelBuddy.objects.update_or_create(
            user=admin_user,
            name=bdata['name'],
            defaults=bdata
        )

    # 6. Sample Reviews for NLP Sentiment Engine
    reviews_data = [
        (dest_objs['Munnar'], 5, "Munnar's misty hills and Kolukkumalai sunrise exceeded all expectations. Incredible stay and delicious tea!", 0.96, "Positive"),
        (dest_objs['Munnar'], 4, "The tea museum and scenic viewpoints were great, though traffic around town was slightly slow.", 0.72, "Positive"),
        (dest_objs['Alappuzha'], 5, "Unbelievable serenity on the houseboat! Fresh Karimeen fish fry was delicious and peaceful sunset.", 0.98, "Positive"),
        (dest_objs['Athirappilly'], 3, "The waterfalls are magnificent during monsoon, but rocky trails can be slippery and crowded on weekends.", 0.45, "Neutral"),
        (dest_objs['Wayanad'], 5, "Banasura dam speedboating and Chembra peak trek were breathtaking. Very hospitable local homestays.", 0.92, "Positive")
    ]
    for dest, rating, text, score, label in reviews_data:
        Review.objects.get_or_create(
            destination=dest,
            user=admin_user,
            review_text=text,
            defaults={'rating': rating, 'sentiment_score': score, 'sentiment_label': label}
        )

    # 7. Document Reminders
    DocumentReminder.objects.get_or_create(
        user=admin_user,
        document_type="Kerala Forest Trek Pass",
        defaults={
            'document_number': 'Eravikulam-E-Pass-2026',
            'expiry_date': today + datetime.timedelta(days=5),
            'notes': 'Booked online for 10:30 AM alpine slot at Rajamala entry point.',
            'is_verified': True
        }
    )

    print("Seeding completed successfully!")

if __name__ == '__main__':
    seed()
