from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # CRUD routes for student records
    path('records/', views.record_list, name='record_list'),
    path('records/add/', views.record_create, name='record_create'),
    path('records/<int:pk>/', views.record_detail, name='record_detail'),
    path('records/<int:pk>/edit/', views.record_update, name='record_update'),
    path('records/<int:pk>/delete/', views.record_delete, name='record_delete'),
    
    # analytics dashboard
    path('analytics/', views.analytics, name='analytics'),
    
    # endpoint to trigger api fetch command
    path('fetch/', views.fetch_data_view, name='fetch_data'),
]