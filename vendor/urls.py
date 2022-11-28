
from django.urls import path, include
from . import views
from accounts.views import vendorDashboard

urlpatterns = [
    path('', vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu-builder'),
    



]