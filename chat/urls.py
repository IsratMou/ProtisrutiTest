# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='home'),
    path('room/<int:room_id>/', views.chat_room, name='room'),
    path('api/rooms/', views.get_chat_rooms, name='api_rooms'),
    path('api/messages/<int:room_id>/', views.get_messages, name='api_messages'),
    path('api/send/', views.send_message, name='api_send'),
]