import os
import csv
import random

os.makedirs('ml/datasets', exist_ok=True)

# 1. destinations_dataset.csv
destinations_data = [
    # name, district, category, climate, budget, popularity, highlights, rating, eco_friendly
    ("Munnar", "Idukki", "Hill Station", "Cool & Misty", 8500, 94, "Tea gardens, Eravikulam National Park, Mattupetty Dam, Anamudi Peak", 4.8, 1),
    ("Alappuzha", "Alappuzha", "Backwaters", "Tropical Coastal", 11000, 92, "Vembanad Lake, Houseboat Cruise, Marari Beach, Pathiramanal", 4.9, 1),
    ("Wayanad", "Wayanad", "Mountain & Nature", "Pleasant & Cool", 7200, 89, "Banasura Sagar Dam, Chembra Peak, Edakkal Caves, Muthanga Wildlife", 4.7, 1),
    ("Vagamon", "Idukki", "Hill Station", "Cool Breeze", 5500, 76, "Pine Forest, Kurisumala Ashram, Green Meadows, Paragliding Point", 4.6, 1),
    ("Thekkady", "Idukki", "Wildlife Sanctuary", "Temperate Forest", 9000, 91, "Periyar Boat Safari, Spice Garden Walk, Bamboo Rafting, Elephant Junction", 4.8, 1),
    ("Athirappilly", "Thrissur", "Waterfalls & Forest", "Humid Tropical", 4500, 78, "Athirappilly Falls, Vazhachal Cascade, Sholayar Rainforest, Chapra Falls", 4.7, 1),
    ("Palakkad", "Palakkad", "Heritage & Valley", "Warm & Breezy", 4800, 75, "Malampuzha Dam, Nelliyampathy Hills, Silent Valley, Dhoni Waterfalls", 4.6, 1),
    ("Marari Beach", "Alappuzha", "Beach & Coastal", "Sea Breeze Tropical", 6500, 71, "Marari Beachfront, Traditional Coir Making, Sea Turtle Hatchery", 4.7, 1),
    ("Nelliyampathy", "Palakkad", "Hill Station", "Misty & Chill", 5200, 68, "Kesavampara View, Seethargundu 1000m Drop, Organic Orange Orchards", 4.6, 1),
    ("Varkala", "Thiruvananthapuram", "Beach & Cliff", "Coastal Warm", 7800, 88, "Varkala Cliff, Papanasam Beach, Janardhana Swami Temple, Watersports", 4.7, 1),
    ("Kozhikode", "Kozhikode", "Heritage & Food", "Coastal Humid", 5000, 82, "Kappad Beach, SM Street, Kozhikode Halwa, Beypore Port, Mananchira", 4.5, 0),
    ("Bekal", "Kasaragod", "Beach & Fort", "Tropical Coastal", 6200, 79, "Bekal Fort, Bekal Beach Park, Kappil Beach, Chandragiri Fort", 4.6, 1),
]

# Generate augmented dataset with slight variations to create 60 rows for KNN training
dest_rows = []
for d in destinations_data:
    dest_rows.append(list(d))
    # Add variations with altered budgets / focus tags
    for i in range(4):
        budget_var = int(d[4] * (1.0 + random.choice([-0.15, -0.08, 0.08, 0.15])))
        pop_var = min(99, max(50, int(d[5] + random.randint(-4, 4))))
        rating_var = round(min(5.0, max(4.0, d[7] + random.choice([-0.1, 0.0, 0.1]))), 1)
        dest_rows.append([f"{d[0]} Spot {i+1}", d[1], d[2], d[3], budget_var, pop_var, d[6], rating_var, d[8]])

with open('ml/datasets/destinations_dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["name", "district", "category", "climate", "average_budget", "popularity_score", "highlights", "rating", "eco_friendly"])
    writer.writerows(dest_rows)

print(f"Created ml/datasets/destinations_dataset.csv with {len(dest_rows)} rows.")


# 2. weather_dataset.csv (Best Time Predictor)
# Kerala weather profile:
# Monsoon: Jun-Aug (heavy rain, high humidity, lower tourist crowd)
# Post-Monsoon/Winter: Oct-Feb (pleasant/cool, low rain, peak tourist crowd, best visit score)
# Summer: Mar-May (warm to hot, pre-monsoon showers)
months = [
    ("Jan", 1), ("Feb", 2), ("Mar", 3), ("Apr", 4), ("May", 5), ("Jun", 6),
    ("Jul", 7), ("Aug", 8), ("Sep", 9), ("Oct", 10), ("Nov", 11), ("Dec", 12)
]

weather_rows = []
dest_names = [d[0] for d in destinations_data]

for dname in dest_names:
    is_hill = dname in ["Munnar", "Wayanad", "Vagamon", "Nelliyampathy"]
    is_beach = dname in ["Alappuzha", "Marari Beach", "Varkala", "Kozhikode", "Bekal"]
    
    for mname, mnum in months:
        if mnum in [12, 1, 2]: # Winter / Peak
            temp = random.uniform(14, 22) if is_hill else random.uniform(22, 29)
            rainfall = random.uniform(5, 25)
            humidity = random.uniform(55, 70)
            crowd = random.randint(4, 5)
            visit_score = random.randint(88, 99)
            label = "Peak"
        elif mnum in [3, 4, 5]: # Summer
            temp = random.uniform(20, 28) if is_hill else random.uniform(28, 35)
            rainfall = random.uniform(30, 90)
            humidity = random.uniform(65, 80)
            crowd = random.randint(2, 4)
            visit_score = random.randint(65, 82)
            label = "Moderate"
        elif mnum in [6, 7]: # Southwest Monsoon
            temp = random.uniform(15, 21) if is_hill else random.uniform(23, 28)
            rainfall = random.uniform(280, 550)
            humidity = random.uniform(85, 98)
            crowd = random.randint(1, 2)
            visit_score = random.randint(35, 55)
            label = "Off-Season"
        elif mnum in [8, 9]: # Late monsoon / Onam
            temp = random.uniform(16, 23) if is_hill else random.uniform(24, 30)
            rainfall = random.uniform(120, 220)
            humidity = random.uniform(75, 88)
            crowd = random.randint(3, 4)
            visit_score = random.randint(70, 86)
            label = "Pleasant"
        else: # Oct, Nov (Post-monsoon)
            temp = random.uniform(15, 22) if is_hill else random.uniform(23, 30)
            rainfall = random.uniform(50, 110)
            humidity = random.uniform(65, 78)
            crowd = random.randint(4, 5)
            visit_score = random.randint(85, 96)
            label = "Peak"
            
        weather_rows.append([
            dname, mname, mnum, round(temp, 1), round(rainfall, 1),
            round(humidity, 1), crowd, visit_score, label
        ])

with open('ml/datasets/weather_dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["destination", "month_name", "month", "avg_temp", "rainfall_mm", "humidity", "crowd_level", "visit_score", "season_label"])
    writer.writerows(weather_rows)

print(f"Created ml/datasets/weather_dataset.csv with {len(weather_rows)} rows.")


# 3. reviews_dataset.csv (Sentiment Analysis)
positive_samples = [
    "Munnar's misty hills and Kolukkumalai sunrise exceeded all expectations. Incredible stay and delicious tea!",
    "Unbelievable serenity on the houseboat! Fresh Karimeen fish fry was delicious and peaceful sunset.",
    "Banasura dam speedboating and Chembra peak trek were breathtaking. Very hospitable local homestays.",
    "Athirappilly waterfalls are stunning in full flow. The lush green forest trail was pure nature therapy.",
    "Vagamon pine forests and green meadows are heavenly. So peaceful and uncrowded, loved every minute.",
    "Varkala cliff sunset view is unforgettable. Great beach cafes, warm hospitality and amazing vibes.",
    "Thekkady Periyar wildlife boat safari was magical. Spotted wild elephants and rare hornbills by the lake.",
    "Marari beach is clean, serene, and free from crowds. Authentic Ayurvedic massage and fresh coconut water.",
    "Palakkad heritage fort and silent valley trek was an enriching experience. Highly recommended for nature lovers.",
    "Nelliyampathy hills offer stunning cloud valley views and orange farm visits. Truly Kerala's best kept secret.",
    "Bekal fort overlooking the Arabian sea is majestic and photogenic. Wonderful sunset walk.",
    "Kozhikode beach sunset combined with authentic paragon biryani and halwa made this trip unforgettable.",
    "Excellent hospitality at our eco-resort. Organic food, clean cottages, and helpful local guides.",
    "Mesmerizing tea plantations as far as the eye can see. Weather was cool, crisp and refreshing.",
    "Floating through the calm Kerala backwaters while sipping fresh tender coconut is pure bliss.",
    "Top Station view in Munnar above the clouds was breathtaking. A must-visit spot in South India.",
    "The trek to Chembra heart-shaped lake was exhilarating. Beautiful mist and clear mountain breeze.",
    "Very safe for solo female travellers. Locals were extremely courteous, polite and helpful.",
    "Great eco-tourism initiatives and zero plastic policy in Periyar sanctuary. Very commendable.",
    "The Ayurvedic spa rejuvenation package was wonderful and refreshed my mind completely."
]

negative_samples = [
    "Extremely crowded, noisy and traffic on the ghat road was completely choked for three hours.",
    "The hotel room was dirty, bathrooms were not cleaned, and bedsheets had bad smell.",
    "Very disappointing boat tour. Boat engine broke down and staff was rude and uncooperative.",
    "Overpriced food and poor hygiene. We had stomach upset after eating at the tourist restaurant.",
    "Rained heavily all day, roads were slippery and dangerous, and most viewpoints were closed.",
    "Waste of money. Hidden charges everywhere and auto drivers demanded double the normal meter rate.",
    "The waterfall was dry and tourist crowd made taking photos impossible. Not worth the drive.",
    "Terrible customer service. Booking was cancelled without notice and no refund was provided.",
    "Plastic waste scattered along the trekking trail. Very poor maintenance by local authorities.",
    "Mosquitoes everywhere and AC in the houseboat was not working during the hot humid night.",
    "Road condition between Munnar and Gap Road was terrible with big potholes and construction dust.",
    "The tour guide was impatient, uninformative and rushed through all attractions in an hour.",
    "Food quality was awful and service took over 45 minutes for a simple cup of tea.",
    "Beach was dirty with plastic bottles and stray dogs. Felt unsafe walking around at night.",
    "Overhyped destination. Parking fees were exorbitant and facilities were completely lacking."
]

neutral_samples = [
    "The tea museum and scenic viewpoints were great, though traffic around town was slightly slow.",
    "The waterfalls are magnificent during monsoon, but rocky trails can be slippery and crowded on weekends.",
    "Average experience. The boat ride was fine but nothing extraordinary compared to other states.",
    "Decent place for a weekend getaway. Food options were limited but acceptable.",
    "Weather was moderate. Scenic views were partly blocked by dense afternoon fog.",
    "Rooms were clean enough for a night stay, though Wi-Fi connection was intermittent in the hills.",
    "Nice views of the dam, but ticket queues were long. Good for a one-time visit.",
    "Standard tourist package. It covers the major highlights but leaves little time for exploring on foot.",
    "Affordable stay with basic amenities. Breakfast was simple South Indian fare.",
    "The beach is okay for an evening stroll, though water currents are somewhat strong for swimming."
]

reviews_rows = []
for _ in range(3):
    for text in positive_samples:
        reviews_rows.append([text, "Positive", random.randint(4, 5)])
    for text in negative_samples:
        reviews_rows.append([text, "Negative", random.randint(1, 2)])
    for text in neutral_samples:
        reviews_rows.append([text, "Neutral", 3])

random.shuffle(reviews_rows)

with open('ml/datasets/reviews_dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["review_text", "sentiment", "rating"])
    writer.writerows(reviews_rows)

print(f"Created ml/datasets/reviews_dataset.csv with {len(reviews_rows)} rows.")


# 4. cost_dataset.csv (AI Travel Cost Optimizer)
# Predicting total trip cost based on destination, days, num_travelers, accommodation_tier, transport_mode
acc_rates = {"Budget Homestay": 1400, "Standard Hotel": 2800, "Luxury Resort": 6500, "Eco Villa": 4200}
trans_rates = {"Public KSRTC": 350, "Shared Cab": 900, "Private Sedan": 2400, "Self Drive SUV": 3600}
food_per_day = 800
activity_per_day = 600

cost_rows = []
for d in dest_names:
    for days in [2, 3, 4, 5, 7]:
        for travelers in [1, 2, 4]:
            for acc_name, acc_price in acc_rates.items():
                for trans_name, trans_price in trans_rates.items():
                    rooms = (travelers + 1) // 2
                    stay_cost = days * rooms * acc_price
                    trans_cost = days * trans_price
                    food_cost = days * travelers * food_per_day
                    act_cost = days * travelers * activity_per_day
                    # Add destination factor and minor random noise
                    dest_mult = 1.15 if d in ["Munnar", "Alappuzha"] else 0.95
                    total = int((stay_cost + trans_cost + food_cost + act_cost) * dest_mult + random.randint(-400, 400))
                    cost_rows.append([d, days, travelers, acc_name, trans_name, total])

# Sample 150 diverse rows
sampled_costs = random.sample(cost_rows, min(160, len(cost_rows)))

with open('ml/datasets/cost_dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["destination", "days", "travelers", "accommodation_type", "transport_type", "total_cost"])
    writer.writerows(sampled_costs)

print(f"Created ml/datasets/cost_dataset.csv with {len(sampled_costs)} rows.")
