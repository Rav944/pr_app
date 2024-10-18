from unittest.mock import patch, MagicMock

from chat.models import Image
from django.core.management import call_command, CommandError
from django.test import TestCase
from requests.exceptions import RequestException


class FetchImagesCommandTest(TestCase):

    @patch('requests.get')
    def test_fetch_images_success(self, mock_get):
        """
        Test the successful fetching of images from the external API and creation of Image objects.
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'total_photos': 2,
            'photos': [
                {
                    'id': 1,
                    'url': 'https://example.com/image1.jpg',
                    'title': 'Test Image 1',
                    'description': 'Description for test image 1'
                },
                {
                    'id': 2,
                    'url': 'https://example.com/image2.jpg',
                    'title': 'Test Image 2',
                    'description': 'Description for test image 2'
                }
            ]
        }
        mock_get.return_value = mock_response

        call_command('fetch_images')

        self.assertEqual(Image.objects.count(), 2)

        image1 = Image.objects.get(url='https://example.com/image1.jpg')
        image2 = Image.objects.get(url='https://example.com/image2.jpg')

        self.assertEqual(image1.title, 'Test Image 1')
        self.assertEqual(image1.description, 'Description for test image 1')
        self.assertEqual(image2.title, 'Test Image 2')
        self.assertEqual(image2.description, 'Description for test image 2')

    @patch('requests.get')
    def test_fetch_images_empty_response(self, mock_get):
        """
        Test fetching images when the API returns no photos.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'total_photos': 0,
            'photos': []
        }
        mock_get.return_value = mock_response

        call_command('fetch_images')

        self.assertEqual(Image.objects.count(), 0)

    @patch('requests.get')
    def test_fetch_images_api_failure(self, mock_get):
        """
        Test handling of a RequestException when the API request fails.
        """
        mock_get.side_effect = RequestException("API request failed")

        with self.assertRaises(CommandError):
            call_command('fetch_images')

        self.assertEqual(Image.objects.count(), 0)
