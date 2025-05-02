
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, CounselorRegistrationForm
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CustomUser.objects.get(email=email)
        if user.check_password(password):
            login(request, user)
            return redirect('dashboard')
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
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register_user.html', {'form': form})

def register_counselor(request):
    if request.method == 'POST':
        form = CounselorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'counselor'
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CounselorRegistrationForm()
    return render(request, 'accounts/register_counselor.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.user_type == 'victim':
        return render(request, 'accounts/user_dashboard.html')
    elif request.user.user_type == 'counselor':
        return render(request, 'accounts/counselor_dashboard.html')
    else:
        return redirect('admin:index')