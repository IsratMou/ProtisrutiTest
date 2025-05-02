# counseling/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def counseling_home(request):
    context = {
        'title': 'Counseling Dashboard'
    }
    return render(request, 'counseling/home.html', context)