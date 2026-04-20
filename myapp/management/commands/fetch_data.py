import requests
from django.core.management.base import BaseCommand

from myapp.models import Location, WeatherRecord

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "Tallahassee": {"latitude": 30.4383, "longitude": -84.2807},
    "Miami": {"latitude": 25.7617, "longitude": -80.1918},
    "Orlando": {"latitude": 28.5383, "longitude": -81.3792},
}


class Command(BaseCommand):
    help = "Fetches current Open-Meteo forecast data and stores daily max temperatures."

    def handle(self, *args, **options):
        for city_name, coordinates in CITIES.items():
            params = {
                "latitude": coordinates["latitude"],
                "longitude": coordinates["longitude"],
                "daily": "temperature_2m_max",
                "timezone": "America/New_York",
            }

            try:
                response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
                response.raise_for_status()
            except requests.RequestException as exc:
                self.stderr.write(self.style.ERROR(f"Failed to fetch {city_name}: {exc}"))
                continue

            daily = response.json().get("daily", {})
            dates = daily.get("time", [])
            temperatures = daily.get("temperature_2m_max", [])
            location, _ = Location.objects.get_or_create(name=city_name)

            saved_count = 0
            for record_date, temperature in zip(dates, temperatures):
                _, created = WeatherRecord.objects.update_or_create(
                    location=location,
                    date=record_date,
                    defaults={"temperature": temperature, "source": "api"},
                )
                if created:
                    saved_count += 1

            self.stdout.write(
                self.style.SUCCESS(f"Synced {city_name}: {saved_count} new weather records.")
            )
