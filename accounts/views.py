from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, CounselorRegistrationForm
from .models import CustomUser, UserProfile, CounselorProfile

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Use authenticate instead of manual email lookup
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'victim'
            user.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register_user.html', {'form': form})

def register_counselor(request):
    if request.method == 'POST':
        form = CounselorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = CounselorRegistrationForm()
    return render(request, 'accounts/register_counselor.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.user_type == 'victim':
        try:
            profile = request.user.user_profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        return render(request, 'accounts/user_dashboard.html', {'profile': profile})
    
    elif request.user.user_type == 'counselor':
        try:
            profile = request.user.counselor_profile
        except CounselorProfile.DoesNotExist:
            # This shouldn't happen if registration is working properly
            return redirect('home')
        return render(request, 'accounts/counselor_dashboard.html', {'profile': profile})
    
    else:  # admin
        return redirect('admin:index')