from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking
from destinations.models import Destination


class UserDashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='anusree')
        self.destination = Destination.objects.create(
            name='Munnar',
            district='Idukki',
            category='Hill Station',
            description='Tea gardens and mountain views.',
        )

    @patch('accounts.views.recommend_destinations', return_value=[])
    def test_dashboard_uses_actual_unique_destination_count_and_username(self, _recommend):
        Destination.objects.create(
            name=' munnar ',
            district='idukki',
            category='Hill Station',
            description='Duplicate destination record.',
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('user_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_destinations'], 1)
        self.assertEqual(len(response.context['featured_destinations']), 1)
        self.assertContains(response, 'View All (1)')
        self.assertNotContains(response, 'View All (9)')
        self.assertContains(response, 'Welcome back, anusree!')
        self.assertNotContains(response, 'anusree Sharma')

    @patch('accounts.views.recommend_destinations')
    def test_dashboard_does_not_repeat_recommendations_in_featured_destinations(self, recommend):
        recommend.return_value = [
            {'destination': self.destination, 'match_percentage': 90, 'reason': 'Match'},
            {'destination': self.destination, 'match_percentage': 85, 'reason': 'Duplicate match'},
        ]
        self.client.force_login(self.user)

        response = self.client.get(reverse('user_dashboard'))

        self.assertEqual(len(response.context['featured_destinations']), 1)
        self.assertEqual(response.context['ai_recommendations'], [])

    @patch('accounts.views.recommend_destinations', return_value=[])
    def test_dashboard_does_not_show_another_users_booking(self, _recommend):
        other_user = User.objects.create_user(username='another-traveller')
        Booking.objects.create(
            user=other_user,
            destination=self.destination,
            travel_date=timezone.localdate() + timedelta(days=4),
            total_amount=1000,
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('user_dashboard'))

        self.assertIsNone(response.context['upcoming_booking'])
        self.assertContains(response, 'No upcoming trips')
