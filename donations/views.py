# donations/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DonationForm
from .models import Donation

def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            if request.user.is_authenticated:
                donation.donor = request.user
            donation.save()
            return redirect('donations:success')
    else:
        form = DonationForm()
    
    return render(request, 'donations/donate.html', {'form': form})

def donation_success(request):
    return render(request, 'donations/donation_success.html')

@login_required
def donation_history(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-donation_date')
    return render(request, 'donations/history.html', {'donations': donations})