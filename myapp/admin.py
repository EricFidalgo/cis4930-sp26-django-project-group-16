from django.contrib import admin
from .models import Location, StudentPerformance, WeatherRecord

# Register basic models
admin.site.register(Location)

# register models here so we can manage them in the /admin dashboard
@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    # added search and filter options to make checking the data easier
    list_display = ('location', 'hours_studied', 'exam_score', 'parental_education')
    list_filter = ('parental_education', 'location')
    search_fields = ('location__name',)

@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ('location', 'date', 'temperature', 'source')
    list_filter = ('source', 'date')
    search_fields = ('location__name',)