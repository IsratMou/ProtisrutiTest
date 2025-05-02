# donations/urls.py
from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.donate, name='donate'),
    path('success/', views.donation_success, name='success'),
    path('history/', views.donation_history, name='history'),
]