from django.contrib import admin
from .models import Rating

# Register your models here.

class RatingAdmin(admin.ModelAdmin):
    list_display = ['food_item','user','rate_value','comment','created_at','updated_at']

admin.site.register(Rating,RatingAdmin)

