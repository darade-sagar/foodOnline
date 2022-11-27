
from django.urls import path, include
from . import views
from accounts.views import vendorDashboard

urlpatterns = [
    path('profile/', views.vprofile, name='vprofile'),
    path('', vendorDashboard, name='vendor'),
    



]