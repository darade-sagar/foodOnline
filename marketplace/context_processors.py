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

def get_cart_amounts(request):
    subtotal,tax,grand_total=0,0,0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id) #type:ignore
            subtotal += fooditem.price*item.quantity

        grand_total += subtotal + tax 
    return dict(subtotal=subtotal,tax=tax, grand_total=grand_total)
