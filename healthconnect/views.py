from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation 
from django.core.exceptions import ValidationError 
from django.contrib.auth.decorators import login_required 

from healthconnect.models import HealthConnectUsers 


def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def help(request):
    return render(request, 'help.html')

def about(request):
    return render(request, 'about.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('user')
        
    if request.method == 'POST':
        try:
            # Create user
            user = HealthConnectUsers.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                username=request.POST.get('username'),
            )
            user.set_password(request.POST.get('password'))
            user.save()

        
            messages.success(request, 'You have successfully created an account. Please log in.')
            return redirect('login') 

        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return redirect('signup')

    return render(request, 'sign-up.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('user')

    if request.method == 'POST':
        username_or_email = request.POST.get('username') 
        password = request.POST.get('password')

        user = None
        if '@' in username_or_email:
            user = HealthConnectUsers.objects.filter(email=username_or_email).first()
        else:
            user = HealthConnectUsers.objects.filter(username=username_or_email).first()
        
        if user and user.check_password(password): 
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('user')
        else:
            messages.error(request, 'Invalid Email/Username or Password.')
            
    return render(request, 'log-in.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Sad to see you leave {user.first_name},\n we'll be glad to have you back,log back in anytime,anywhere!!!!")
    return redirect('index')

# --- Protected Views ---

@login_required(login_url='login')
def user(request):
    return render(request, 'user.html')

@login_required(login_url='login')
def bookings(request):
    return render(request, 'bookings.html')

@login_required(login_url='login')
def admin_panel(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('user') 
    healthconnect_users = HealthConnectUsers.objects.all()
    return render(request, 'admin.html', {'healthconnect_users': healthconnect_users})

@login_required(login_url='login')
def book_appointment_submit(request):
    if request.method == 'POST':
        messages.success(request, "Your appointment has been successfully booked!")
        return redirect('user')
    return redirect('booking')