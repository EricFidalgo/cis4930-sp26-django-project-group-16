import json
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.management import call_command
from .models import StudentPerformance, WeatherRecord
from .forms import StudentPerformanceForm
from django.views.decorators.http import require_POST

# basic landing page
def home(request):
    return render(request, 'myapp/home.html')

# show all records
def record_list(request):
    records = StudentPerformance.objects.all()
    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/list.html', {'page_obj': page_obj})

# view a single record's details
def record_detail(request, pk):
    record = get_object_or_404(StudentPerformance, pk=pk)
    return render(request, 'myapp/detail.html', {'record': record})

# handle creating new student records
def record_create(request):
    if request.method == 'POST':
        form = StudentPerformanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = StudentPerformanceForm()
    return render(request, 'myapp/form.html', {'form': form})

# standard update view, reuses the form template
def record_update(request, pk):
    record = get_object_or_404(StudentPerformance, pk=pk)
    if request.method == 'POST':
        form = StudentPerformanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = StudentPerformanceForm(instance=record)
    return render(request, 'myapp/form.html', {'form': form})

# delete confirmation
def record_delete(request, pk):
    record = get_object_or_404(StudentPerformance, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('record_list')
    return render(request, 'myapp/confirm_delete.html', {'record': record})

def analytics(request):
    # pulling in location__name for the third aggregation chart
    qs = StudentPerformance.objects.values('hours_studied', 'exam_score', 'parental_education', 'location__name')
    df = pd.DataFrame(list(qs))
    
    # handle case where db is empty so it doesn't crash
    if df.empty:
        return render(request, 'myapp/analytics.html', {
            'summary': {}, 'bar_json': '{}', 'scatter_json': '{}', 'study_line_json': '{}'
        })

    # 1. average score based on parents' education level
    avg_scores_parent = df.groupby('parental_education')['exam_score'].mean()
    bar_chart_data = {
        'labels': avg_scores_parent.index.tolist(),
        'values': avg_scores_parent.values.tolist(),
    }
    
    # 2. bucket study hours into groups of 10
    bins = [0, 10, 20, 30, 40, 50]
    labels = ["1-10", "11-20", "21-30", "31-40", "41-50"]
    df['study_band'] = pd.cut(df['hours_studied'], bins=bins, labels=labels)
    # fillna(0) just in case a band has no students
    avg_scores_study = df.groupby('study_band', observed=False)['exam_score'].mean().fillna(0)
    
    study_line_data = {
        'labels': avg_scores_study.index.tolist(),
        'values': avg_scores_study.values.tolist(),
    }

    # 3. see if location affects scores
    avg_scores_location = df.groupby('location__name')['exam_score'].mean()
    location_summary = avg_scores_location.round(2).to_dict()

    scatter_data = {
        'x': df['hours_studied'].tolist(),
        'y': df['exam_score'].tolist()
    }
    
    # pass everything to frontend as json strings for the charts
    return render(request, 'myapp/analytics.html', {
        'bar_json': json.dumps(bar_chart_data),
        'scatter_json': json.dumps(scatter_data),
        'study_line_json': json.dumps(study_line_data),
        'location_summary': location_summary,
        'summary': df.describe().round(2).to_dict()
    })

# trigger the custom management command to pull api data
@require_POST
def fetch_data_view(request):
    # only let staff run this so randoms don't spam the api
    if request.user.is_staff:
        call_command('fetch_data')
    return redirect('home')