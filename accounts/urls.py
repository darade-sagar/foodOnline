from django.urls import path, include
from . import views


urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('myAccount/', views.myAccount, name='myAccount'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),


]