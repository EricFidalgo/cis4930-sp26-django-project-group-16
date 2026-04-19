from django import forms
from .models import StudentPerformance

class StudentPerformanceForm(forms.ModelForm):
    class Meta:
        model = StudentPerformance
        fields = '__all__'
        widgets = {
            'location': forms.Select(attrs={'class': 'form-select'}),
            'hours_studied': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'parental_education': forms.Select(attrs={'class': 'form-select'}),
        }