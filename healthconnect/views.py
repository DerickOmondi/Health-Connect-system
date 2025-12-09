from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password 
from django.contrib.auth import password_validation 
from django.core.exceptions import ValidationError 

from healthconnect.models import HealthConnectUsers 


def services(request):
    """Renders the services page."""
    return render(request, 'services.html')


def index(request):
    """Renders the homepage."""
    return render(request, 'index.html') 

def user(request):
    """Renders the authenticated user's dashboard."""
    if request.user.is_authenticated:
        return render(request, 'user.html')
    else:
        return redirect('login') 

def admin_panel(request):
    """Renders the admin panel (consider adding a staff/superuser check)."""
    healthconnect_users = HealthConnectUsers.objects.all()
    return render(request, 'admin.html', {'healthconnect_users': healthconnect_users})



def signup(request):
    """Handles user registration and password complexity validation."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        other_names = request.POST.get('other_names')
        email = request.POST.get('email')
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        
   
        try:
            password_validation.validate_password(raw_password, user=None)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('signup') 
        
      
        try:
            HealthConnectUsers.objects.create_user(
                email=email,
                username=username,
                password=raw_password,
                first_name=first_name,
                last_name=last_name,
                other_names=other_names
            )
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Registration failed. User/Email may already exist. Error: {e}')
            return redirect('signup')
    
    return render(request, 'sign-up.html')


def logout_view(request):
    """Logs the user out and clears the session."""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been logged out successfully.")
    return redirect('index')

# In healthconnect/views.py

def login_view(request):
    """Handles user login and session creation."""
    if request.method == 'POST':
        username_or_email = request.POST.get('username') 
        password = request.POST.get('password')

        user = None
        # Attempt to find user by email
        try:
            user = HealthConnectUsers.objects.get(email=username_or_email)
        except HealthConnectUsers.DoesNotExist:
            # If not found by email, attempt to find by username
            try:
                user = HealthConnectUsers.objects.get(username=username_or_email)
            except HealthConnectUsers.DoesNotExist:
                pass 
        
       
        if user and user.check_password(password): 
         
            login(request, user) 
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('user')
        else:
            messages.error(request, 'Invalid Email/Username or Password.')
            return render(request, 'log-in.html') 

    return render(request, 'log-in.html')