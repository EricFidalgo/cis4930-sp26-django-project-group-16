import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import WeatherRecord, Location
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch latest data from the weather API (Project 2)'

    def handle(self, *args, **options):
        # coordinates mapping for the required cities
        locations = {
            'Tallahassee': {'lat': 30.4383, 'lon': -84.2807},
            'Miami': {'lat': 25.7617, 'lon': -80.1918},
            'Orlando': {'lat': 28.5383, 'lon': -81.3792}
        }
        
        for city_name, coords in locations.items():
            try:
                # hitting the open-meteo api for hourly temps
                resp = requests.get(
                    'https://api.open-meteo.com/v1/forecast',
                    params={'latitude': coords['lat'], 'longitude': coords['lon'], 'hourly': 'temperature_2m'},
                    timeout=10
                )
                resp.raise_for_status()
                data = resp.json()
                
                loc, _ = Location.objects.get_or_create(name=city_name)
                
                # wrap in a transaction so if it crashes mid-loop we don't get partial data
                with transaction.atomic():
                    for i, temp in enumerate(data['hourly']['temperature_2m'][:24]):
                        date_str = data['hourly']['time'][i][:10]
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        
                        WeatherRecord.objects.update_or_create(
                            location=loc,
                            date=date_obj,
                            defaults={'temperature': temp, 'source': 'api'}
                        )
                self.stdout.write(self.style.SUCCESS(f'Fetched API data for {city_name}'))
            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.ERROR(f'Error fetching {city_name}: {e}'))