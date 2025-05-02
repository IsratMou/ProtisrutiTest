# counseling/urls.py
from django.urls import path
from . import views

app_name = 'counseling'  # This is for namespace

urlpatterns = [
    path('', views.counseling_home, name='home'),
    # We'll add more paths here later
]
