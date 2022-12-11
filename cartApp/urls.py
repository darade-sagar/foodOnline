from  django.urls import path
from . import views

urlpatterns = [
    path('',views.cart_page, name='cart_page'),
    path('increase/<int:id>',views.inc_cart, name='inc_cart'),
    path('decrease/<int:id>',views.dec_cart, name='dec_cart'),
    path('delete/<int:id>',views.delete_cart, name='delete_cart'),

]
