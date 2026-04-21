from django.test import TestCase, Client
from django.urls import reverse
from .models import Location, StudentPerformance

class StudentAppTests(TestCase):
    
    def setUp(self):
        # setting up some dummy data for testing
        self.location = Location.objects.create(name="Test Campus")
        self.performance = StudentPerformance.objects.create(
            location=self.location,
            hours_studied=10.5,
            exam_score=85.0,
            parental_education='college'
        )
        self.client = Client()

    def test_model_creation(self):
        # check to see if the model saves correctly
        # print("Testing model creation...") 
        loc = Location.objects.get(name="Test Campus")
        self.assertEqual(loc.name, "Test Campus")
        self.assertEqual(self.performance.hours_studied, 10.5)

    def test_homepage_view(self):
        # making sure the home page actually loads
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Student Performance") # check if title is there

    def test_list_view(self):
        # checking the list page
        response = self.client.get(reverse('record_list'))
        self.assertEqual(response.status_code, 200)