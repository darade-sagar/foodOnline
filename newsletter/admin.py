from django.contrib import admin
from .models import SubscribedMails,News
# Register your models here.
class SubscribedMailsAdmin(admin.ModelAdmin):
    list_display = ['email','is_active','created_at']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','short_description','created_by','created_at','updated_at']
    prepopulated_fields = {'slug':('title',)}

    
admin.site.register(SubscribedMails,SubscribedMailsAdmin)
admin.site.register(News,NewsAdmin)
