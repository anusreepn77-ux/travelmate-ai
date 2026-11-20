import binascii
import struct
from tempfile import TemporaryDirectory
import zlib

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Destination


def tiny_png():
    def chunk(kind, data):
        contents = kind + data
        return (
            struct.pack('>I', len(data))
            + contents
            + struct.pack('>I', binascii.crc32(contents) & 0xFFFFFFFF)
        )

    header = struct.pack('>2I5B', 1, 1, 8, 2, 0, 0, 0)
    return (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', header)
        + chunk(b'IDAT', zlib.compress(b'\x00\xff\x00\x00'))
        + chunk(b'IEND', b'')
    )


class AdminDestinationsViewTests(TestCase):
    def setUp(self):
        self.media_dir = TemporaryDirectory()
        self.addCleanup(self.media_dir.cleanup)
        self.media_settings = override_settings(MEDIA_ROOT=self.media_dir.name)
        self.media_settings.enable()
        self.addCleanup(self.media_settings.disable)
        self.admin = User.objects.create_user(
            username='admin',
            password='test-password',
            is_staff=True,
        )
        self.destination = Destination.objects.create(
            name='Munnar',
            district='Idukki',
            category='Hill Station',
            description='Tea gardens and mountain views.',
        )

    def test_admin_destination_page_uses_admin_layout(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('admin_destinations'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard/destinations.html')
        self.assertTemplateUsed(response, 'admin_base.html')
        self.assertContains(response, self.destination.name)
        self.assertContains(response, reverse('edit_destination', args=[self.destination.pk]))
        self.assertNotContains(response, 'Django Superuser')

    def test_admin_destination_page_requires_staff_login(self):
        response = self.client.get(reverse('admin_destinations'))

        self.assertEqual(response.status_code, 302)

    def test_create_package_page_has_visible_add_action(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('create_package'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Travel Package')
        self.assertContains(response, 'class="btn btn-success py-2 fw-bold"')

    def test_traveler_destination_page_keeps_traveler_layout(self):
        response = self.client.get(reverse('destination_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'destinations/destination_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_admin_can_create_destination_with_uploaded_image(self):
        self.client.force_login(self.admin)
        image = SimpleUploadedFile(
            'vagamon.png',
            tiny_png(),
            content_type='image/png',
        )

        response = self.client.post(
            reverse('add_destination'),
            {
                'name': 'Vagamon',
                'district': 'Idukki',
                'category': 'Hill Station',
                'average_budget': '5500',
                'description': 'Pine forests and meadows.',
                'image': image,
            },
        )

        self.assertRedirects(response, reverse('admin_dashboard'))
        destination = Destination.objects.get(name='Vagamon')
        self.assertTrue(destination.image.name.endswith('vagamon.png'))
        self.assertTrue(destination.image.storage.exists(destination.image.name))

    def test_admin_can_replace_destination_image(self):
        self.client.force_login(self.admin)
        image = SimpleUploadedFile(
            'munnar.png',
            tiny_png(),
            content_type='image/png',
        )

        response = self.client.post(
            reverse('edit_destination', args=[self.destination.pk]),
            {
                'name': self.destination.name,
                'district': self.destination.district,
                'category': self.destination.category,
                'average_budget': '5500',
                'description': self.destination.description,
                'image': image,
            },
        )

        self.assertRedirects(response, reverse('admin_dashboard'))
        self.destination.refresh_from_db()
        self.assertTrue(self.destination.image.name.endswith('munnar.png'))

    def test_admin_rejects_non_image_upload(self):
        self.client.force_login(self.admin)
        invalid_file = SimpleUploadedFile(
            'not-an-image.txt',
            b'not an image',
            content_type='text/plain',
        )

        response = self.client.post(
            reverse('add_destination'),
            {
                'name': 'Invalid Image Destination',
                'district': 'Idukki',
                'category': 'Hill Station',
                'average_budget': '5500',
                'description': 'Test upload validation.',
                'image': invalid_file,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload a valid image')
        self.assertFalse(Destination.objects.filter(name='Invalid Image Destination').exists())
