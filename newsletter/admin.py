from django.contrib import admin
from .models import SubscribedMails
# Register your models here.
class SubscribedMailsAdmin(admin.ModelAdmin):
    list_display = ['email','is_active','created_at']

    
admin.site.register(SubscribedMails,SubscribedMailsAdmin)
