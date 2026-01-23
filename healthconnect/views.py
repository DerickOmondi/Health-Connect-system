from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation 
from django.core.exceptions import ValidationError 
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse, Http404
from django.conf import settings
import os

from healthconnect.models import HealthConnectUsers 



def index(request):
    context = {}
    if request.user.is_authenticated:
        context['user_data'] = request.user
    return render(request, 'index.html', context)

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
    messages.info(request, "Logged out successfully!")
    return redirect('index')


@login_required(login_url='login')
def user(request):
    return render(request, 'user.html')

@login_required(login_url='login')
def qr_code_view(request):
    context = {
        'user_data': request.user
    }
    return render(request, 'qr-code.html', context)

@login_required(login_url='login')
def download_qr(request):
    if not request.user.qr_code:
        messages.error(request, "No QR code found to download.")
        return redirect('qr_code')
    
    file_path = request.user.qr_code.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/png")
            response['Content-Disposition'] = f'attachment; filename="QR_{request.user.username}.png"'
            return response
    raise Http404


@login_required(login_url='login')
def admin_panel(request):
    """View for superusers to manage users."""
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('user') 
    healthconnect_users = HealthConnectUsers.objects.all()
    return render(request, 'admin.html', {'healthconnect_users': healthconnect_users})

@login_required(login_url='login')
def bookings(request):
    """View to display user bookings."""
    return render(request, 'bookings.html')

@login_required(login_url='login')
def book_appointment_submit(request):
    """View to handle appointment form submissions."""
    if request.method == 'POST':
        messages.success(request, "Appointment submitted successfully!")
        return redirect('booking')
    return redirect('services')