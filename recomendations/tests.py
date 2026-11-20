from contextlib import ExitStack
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from destinations.models import Destination
from .ml_engine import generate_ai_trip_plan, get_malayalam_translations


class DestinationSpecificAiTests(TestCase):
    def setUp(self):
        Destination.objects.create(
            name='Munnar',
            district='Idukki',
            category='Hill Station',
            description='Tea hills.',
            highlights='Tea Museum, Tea estates',
        )
        Destination.objects.create(
            name='Alappuzha',
            district='Alappuzha',
            category='Backwaters',
            description='Backwater destination.',
            highlights='Punnamada Lake, Houseboat Cruise',
        )

    def test_malayalam_phrases_change_for_selected_destination(self):
        munnar_phrases = get_malayalam_translations(destination_name='Munnar')
        alappuzha_phrases = get_malayalam_translations(destination_name='Alappuzha')

        self.assertNotEqual(
            [phrase['english'] for phrase in munnar_phrases],
            [phrase['english'] for phrase in alappuzha_phrases],
        )
        self.assertEqual(len({phrase['english'] for phrase in alappuzha_phrases}), 3)

    def test_assistant_hub_uses_selected_destination_for_phrases(self):
        empty_results = {
            'recommend_destinations': [],
            'generate_ai_trip_plan': {},
            'predict_best_time': {},
            'get_hidden_gems': [],
            'match_travel_buddies': [],
            'analyze_review_sentiment': {},
            'optimize_travel_cost': {},
            'get_outfit_recommendations': {},
            'calculate_carbon_footprint': {},
            'get_safety_radar': {},
            'calculate_route_matrix': {},
        }
        with ExitStack() as stack:
            for name, result in empty_results.items():
                stack.enter_context(patch(f'recomendations.views.{name}', return_value=result))
            response = self.client.get(
                reverse('assistant_hub'),
                {'dest': 'Alappuzha', 'tab': 'safety'},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_dest'], 'Alappuzha')
        self.assertEqual(
            response.context['translations'][0]['english'],
            'Where can I board the houseboat?',
        )

    @patch('recomendations.ml_engine.call_gemini_api', return_value=None)
    def test_fallback_itinerary_uses_selected_destination_highlights(self, _gemini):
        destination = Destination.objects.get(name='Alappuzha')
        destination.highlights = 'Punnamada Lake, Houseboat Cruise, Alappuzha Beach'
        destination.save()

        itinerary = generate_ai_trip_plan(destination.name, days=2)
        planned_activities = [
            slot['activity']
            for day in itinerary['daily_slots']
            for slot in day['slots']
        ]

        self.assertEqual(itinerary['destination'], destination.name)
        self.assertEqual(
            planned_activities,
            ['Punnamada Lake', 'Houseboat Cruise', 'Alappuzha Beach'],
        )
        self.assertNotIn('Kolukkumalai Sunrise 4x4 Safari & Tea Plucking', planned_activities)
