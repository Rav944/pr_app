import requests
from chat.models import Image
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Fetch all available photos from the external API and create Image models in the database.'

    def handle(self, *args, **kwargs):
        api_url = 'https://api.slingacademy.com/v1/sample-data/photos'
        params = {
            'offset': 0,
            'limit': 10
        }

        try:
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            total_photos = data['total_photos']
            self.stdout.write(self.style.SUCCESS(f"Total photos available: {total_photos}"))

            while params['offset'] < total_photos:
                response = requests.get(api_url, params=params, timeout=30)
                response.raise_for_status()
                images = response.json().get('photos', [])

                if not images:
                    self.stdout.write(self.style.WARNING('No more images to fetch.'))
                    break

                for image_data in images:
                    image_url = image_data['url']
                    image_title = image_data['title']
                    image_description = image_data['description']

                    if not Image.objects.filter(url=image_url).exists():
                        Image.objects.create(
                            url=image_url,
                            title=image_title,
                            description=image_description
                        )
                        self.stdout.write(self.style.SUCCESS(f"Created new image: {image_title}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Image {image_title} already exists in the database."))

                params['offset'] += params['limit']

                if len(images) < params['limit']:
                    self.stdout.write(self.style.SUCCESS('All available images have been fetched.'))
                    break

        except requests.RequestException as e:
            raise CommandError(f'Error fetching images from API: {e}')
