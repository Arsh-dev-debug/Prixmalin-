from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register(request):
    if request.user.is_authenticated:
        return redirect('store:home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Use email as username
            user.username = user.email
            user.save()
            
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            # Log in the user automatically
            login(request, user)
            return redirect('store:home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# store/views.py
def contact(request):
    return render(request, 'users/contact.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to get the user by email
        try:
            user = User.objects.get(email=email)
            # If user exists, authenticate with username (which is email in our case)
            user = authenticate(request,username=user.username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('store:home')
        except User.DoesNotExist:
            pass
        
        messages.error(request, 'Invalid email or password')
    
    return render(request, 'users/login.html')