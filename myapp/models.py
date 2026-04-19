from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# simple lookup table so we don't repeat location strings everywhere
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# main student data model
class StudentPerformance(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    # cant have negative hours studying
    hours_studied = models.FloatField(validators=[MinValueValidator(0)])
    # restrict scores between 0 and 100
    exam_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    parental_education = models.CharField(
        max_length=50,
        choices=[
            ('high_school', 'High School'),
            ('college', 'College'),
            ('postgrad', 'Postgraduate'),
            ('none', 'None')
        ]
    )

# storing weather data pulled from the api
class WeatherRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    temperature = models.FloatField()
    # keep track of where this data came from
    source = models.CharField(
        max_length=50, 
        choices=[('api', 'API Fetch'), ('csv', 'CSV Import')],
        default='api'
    )