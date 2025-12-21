from django.contrib import admin
from django.urls import path
from healthconnect import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
    
    path('admin-panel/', views.admin_panel, name='admin_panel'), 
    path('user/', views.user ,name="user"),
    path('signup/', views.signup ,name="signup"), 
    path('login/', views.login_view ,name="login"),
    path('logout/', views.logout_view ,name="logout"), 
    path('services/', views.services ,name="services"),
    path('help/', views.help ,name="help"),
    path('about/', views.about ,name="about"),
    path('bookings/', views.bookings ,name="booking"),
    path('book-appointment-submit/', views.book_appointment_submit ,name="book_appointment"), 
]