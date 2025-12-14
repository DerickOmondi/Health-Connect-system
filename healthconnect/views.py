# healthconnect/views.py

from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password 
from django.contrib.auth import password_validation 
from django.core.exceptions import ValidationError 
# 🌟 NEW: Import the login_required decorator
from django.contrib.auth.decorators import login_required 

from healthconnect.models import HealthConnectUsers 

# --- Public Views (No login required) ---

def index(request):
    """Renders the homepage."""
    return render(request, 'index.html') 

def services(request):
    """Renders the services page."""
    return render(request, 'services.html')

def help(request):
    """Renders the help page."""
    return render(request, 'help.html')

def about(request):
    """Renders the about page."""
    return render(request, 'about.html')

# --- Authentication Views ---

def signup(request):
    """Handles user registration."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        other_names = request.POST.get('other_names')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # 1. Password validation
            password_validation.validate_password(password, user=None)
            
            # 2. Check if username or email already exists
            if HealthConnectUsers.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return redirect('signup')
            if HealthConnectUsers.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return redirect('signup')
                
            # 3. Create the user
            user = HealthConnectUsers.objects.create(
                first_name=first_name,
                last_name=last_name,
                other_names=other_names,
                email=email,
                username=username,
            )
            user.set_password(password)
            user.save()

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login') 
        except ValidationError as e:
            # Handle password validation errors
            for error in list(e.messages):
                messages.error(request, error)
            return redirect('signup')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred. Email may already exist. Error: {e}')
            return redirect('signup')
    
    return render(request, 'sign-up.html')

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
        
        # Check password using the custom user model's check_password
        if user and user.check_password(password): 
         
            login(request, user) 
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('user')
        else:
            messages.error(request, 'Invalid Email/Username or Password.')
            return render(request, 'log-in.html', {'username_attempt': username_or_email}) 
            
    return render(request, 'log-in.html') 


def logout_view(request):
    """Logs the user out and clears the session."""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been logged out successfully.")
    return redirect('index')

# --- Authenticated Views (Require login) ---

@login_required(login_url='login')
def user(request):
    """Renders the authenticated user's dashboard. Protected by @login_required."""
    return render(request, 'user.html')

@login_required(login_url='login')
def admin_panel(request):
    """Renders the admin panel, restricted to superusers. Protected by @login_required."""
    # Good practice: Add an explicit check for superuser status
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access the admin panel.")
        return redirect('user') 
        
    healthconnect_users = HealthConnectUsers.objects.all()
    return render(request, 'admin.html', {'healthconnect_users': healthconnect_users})

@login_required(login_url='login')
def bookings(request):
    """Renders the booking form page (GET request). Protected by @login_required."""
    return render(request, 'bookings.html')
    
@login_required(login_url='login')
def book_appointment_submit(request):
    """Handles the POST request for booking an appointment."""
    if request.method == 'POST':
        # 1. Retrieve data from the form
        specialty = request.POST.get('specialty')
        doctor = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason_for_visit = request.POST.get('reason_for_visit')
        consultation_type = request.POST.get('consultation_type')
        
        # NOTE: Implement your database saving logic here, e.g., 
        # Booking.objects.create(user=request.user, ...)

        # Placeholder successful logic
        print(f"Appointment booked for {request.user.username}: {consultation_type} on {appointment_date} at {appointment_time}.")
        messages.success(request, "Your appointment has been successfully booked!")

        return redirect('user') # Redirect to the user dashboard after success
    
    # If a non-POST request hits this URL (e.g., direct navigation), redirect to the form
    return redirect('booking')