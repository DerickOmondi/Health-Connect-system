from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password 
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class HealthConnectUsersManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, username, password, **extra_fields)

class HealthConnectUsers(AbstractBaseUser): 
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    other_names = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(max_length=30, unique=True, blank=False, null=False) 
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = HealthConnectUsersManager()
    
    def save(self, *args, **kwargs):
        """Overrides the save method to generate a QR code pointing to the homepage."""
        if not self.qr_code:
            # Directs to the local development homepage
            data_to_encode = "http://127.0.0.1:8000/"
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data_to_encode)
            qr.make(fit=True)
            
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Prepare image for storage
            fname = f'qr_code-{self.username}.png'
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            
            self.qr_code.save(fname, File(buffer), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
        
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser