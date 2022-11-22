from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User, UserProfile

class CustomUserAdmin(UserAdmin):
    list_display = ['email','first_name','last_name','username','role','is_active']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ['-date_joined','username']


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
