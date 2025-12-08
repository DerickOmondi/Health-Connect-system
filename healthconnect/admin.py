from django.contrib import admin

# Register your models here.

from .models import HealthConnectUsers

class HealthConnectUsersAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 
        'last_name',
        'other_names',
        'email', 
        'username',
        
    )
    
    list_filter = ('last_name',)
    search_fields = ('first_name', 'last_name','other_names', 'email', 'username')

admin.site.register(HealthConnectUsers, HealthConnectUsersAdmin)