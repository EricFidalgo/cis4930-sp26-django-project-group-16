import csv
from django.core.management.base import BaseCommand
from myapp.models import StudentPerformance, Location

EDUCATION_MAP = {
    "high school": "high_school",
    "college": "college",
    "postgraduate": "postgrad",
    "none": "none",
}

# load the csv data from project 1 so we don't have to enter it manually
class Command(BaseCommand):
    help = 'Loads Project 1 CSV data into the database'

    def handle(self, *args, **options):
        file_path = 'data/raw/StudentPerformanceFactors.csv'
        default_location, _ = Location.objects.get_or_create(name="Default Campus")

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                education = row.get('Parental_Education_Level', 'none').strip().lower()
                StudentPerformance.objects.create(
                    location=default_location,
                    hours_studied=float(row.get('Hours_Studied', 0)),
                    exam_score=float(row.get('Exam_Score', 0)),
                    parental_education=EDUCATION_MAP.get(education, 'none')
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded Student Performance data.'))
