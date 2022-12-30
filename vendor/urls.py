
from django.urls import path, include
from . import views
from accounts.views import vendorDashboard

urlpatterns = [
    path('', vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu-builder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),
    
    # CRUD Category
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>', views.delete_category, name='delete_category'),
    

    # CRUD Food
    path('menu-builder/food/add/', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>', views.delete_food, name='delete_food'),
    
    # Opening Hours
    path('opening-hours', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>', views.remove_opening_hours, name='remove_opening_hours'),

    path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    path('my_orders/', views.my_orders, name='vendor_my_orders'),

]