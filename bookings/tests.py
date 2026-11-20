from django.test import TestCase
from django.urls import reverse

from .views import _deduplicate_services


class NearbyPlacesTests(TestCase):
    def test_duplicate_services_are_removed_without_reordering(self):
        first = {
            'name': 'City Hospital',
            'type': 'Hospital',
            'contact': '111',
        }
        duplicate = {
            'name': ' city hospital ',
            'type': 'HOSPITAL',
            'contact': '222',
        }
        other = {
            'name': 'Care Pharmacy',
            'type': 'Pharmacy',
            'contact': '333',
        }

        self.assertEqual(_deduplicate_services([first, duplicate, other]), [first, other])

    def test_unknown_destination_does_not_show_another_destination_services(self):
        response = self.client.get(
            reverse('nearby_places'),
            {'dest': 'Unknown Place', 'type': 'Hospital'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No nearby places matched the selected filter.')
        self.assertNotContains(response, 'Devikulam Primary Health Centre')

    def test_destination_and_category_filters_show_matching_service_once(self):
        response = self.client.get(
            reverse('nearby_places'),
            {'dest': 'Wayanad', 'type': 'Hospital'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode().count(
                '<h6 class="fw-bold mb-1">Wayanad District Hospital Mananthavady</h6>'
            ),
            1,
        )
        self.assertNotContains(response, 'CareWell Meds Sulthan Bathery')
