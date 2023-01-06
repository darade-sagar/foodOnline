from  django.urls import path
from . import views

urlpatterns = [
    path('',views.marketplace, name='marketplace'),
    path('vendor/<slug:vendor_slug>/',views.vendor_detail, name='vendor_detail'),
    path('product/product-info/<int:id>',views.product_info, name='product_info'),
    
    # ADD to Cart
    path('add_to_cart/<int:food_id>',views.add_to_cart, name='add_to_cart'),
    # dec cart
    path('decrease_cart/<int:food_id>',views.decrease_cart, name='decrease_cart'),
    # delete cart
    path('delete_cart/<int:cart_id>',views.delete_cart, name='delete_cart'),


]
