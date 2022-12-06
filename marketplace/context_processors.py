from .models import Cart
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count=0
    dict = {}
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            for cartitem in cart_items:
                cart_count += cartitem.quantity
        except:
            cart_count=0
    dict['cart_count'] = cart_count
    return dict
