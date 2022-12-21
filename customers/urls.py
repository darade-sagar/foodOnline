from django.urls import path, include
from . import views
from accounts.views import custDashboard

urlpatterns = [
    path('', custDashboard, name='customer'),
    path('profile/', views.cprofile, name='cprofile'),
]
