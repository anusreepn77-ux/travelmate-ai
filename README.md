# TravelMate AI — Explore More. Plan Smarter. Travel Better.

> **AI-Powered Travel Planning System for Kerala Tourism**  
> Advanced Full-Stack Academic Project — Group 6

---

## 🌟 Overview
**TravelMate AI** is an intelligent travel planning web application designed to simplify the entire travel journey for Kerala tourism. It delivers two decoupled dashboards:
- **Admin Control Center**: Comprehensive operations suite with booking fulfillment, inventory management, customer analytics, and real-time AI vitality tracking.
- **Traveller Dashboard**: Intuitive consumer interface with personalized ML recommendations, live generative AI trip planning, expense pool tracking, digital QR vouchers, and buddy matching.

---

## 🚀 Key Features

### 🧠 11 AI & ML Intelligence Features
1. **Smart Destination Recommendation** — TF-IDF content extraction + K-Nearest Neighbors ($k=5$, Cosine similarity).
2. **AI Trip Planner** — Generative AI day-by-day time-slotted itinerary generator using Google Gemini API.
3. **Best Time to Visit Predictor** — Weather telemetry classification & regression using Random Forest (100% accuracy) & Decision Trees.
4. **Hidden Tourist Places Finder** — Content-based recommender filtering tranquil, low-crowd destinations.
5. **Travel Buddy Matching** — Vector-space compatibility matching for solo travelers.
6. **Tourist Review Sentiment Analysis** — NLP classification pipeline (TF-IDF + Logistic Regression).
7. **AI Travel Cost Optimizer** — Random Forest regression ($R^2 = 0.9722$) with stay/transit cost-saving breakdowns.
8. **AI Outfit & Packing Stylist** — Altitude and climate-aware packing blueprints.
9. **Malayalam Dialect Voice & Text AI** — English-to-Malayalam translation with script, phonetic transliteration, and cultural tips.
10. **Sustainable Travel Footprint** — Carbon emission calculator with certified solar eco-stay recommendations.
11. **Travel Safety Score Radar** — Hazard radar, road condition advisories, and emergency SOS routing (112, 108, 1091).

### 🛠️ 3 Smart Utility Modules
- **Module A: Nearby Places Finder** — Verified local directory of hospitals, pharmacies, 24/7 ATMs, and restaurants with Google Maps routing.
- **Module B: Travel Document Reminder** — Pass & visa expiry tracking with document checklist.
- **Module C: Multi-Destination Route Explorer** — Inter-district Kerala transit matrix with road distance, travel duration, and fuel/cab budget estimation.

---

## 🏗️ Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons |
| **Backend** | Python 3.14, Django 6.1 |
| **Database** | PostgreSQL (`travelmate_db`) |
| **Machine Learning** | Scikit-learn, Pandas, NumPy, Joblib |
| **Generative AI** | Google Gemini Live API |

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/anusreepn77-ux/travelmate-ai.git
cd travelmate-ai
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv env
# On Windows:
.\env\Scripts\activate
# On Linux/macOS:
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_secret_key_here
DEBUG=True
GEMINI_API_KEY=your_google_gemini_api_key
```

### 5. Run Migrations & Seed Database
```bash
python manage.py migrate
python seed_data.py
```

### 6. Start Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🔑 Default Credentials
- **Admin Control Center**: `admin` / `admin123` (`http://127.0.0.1:8000/admin-dashboard/`)
- **Demo Traveller**: `ananya_patel` / `admin123`
