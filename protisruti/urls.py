
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('counseling/', include('counseling.urls')),
    path('chat/', include('chat.urls')),
    path('donations/', include('donations.urls')),
]
