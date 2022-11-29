
from django.urls import path, include
from . import views
from accounts.views import vendorDashboard

urlpatterns = [
    path('', vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu-builder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),
    



]