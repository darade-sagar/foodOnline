from .models import Cart,Tax
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
    subtotal,grand_total=0,0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id) #type:ignore
            subtotal += fooditem.price*item.quantity

        get_tax = Tax.objects.filter(is_active=True)
        tax_dict = {}
        total_tax = 0
        for i in get_tax:
            tax_type = i.tax_type 
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal)/100,2)
            
            # {'CGST':{'8.00','11.12'}}
            tax_dict[tax_type] = {str(tax_percentage):str(tax_amount)}
            
            total_tax += tax_amount

        grand_total += subtotal + total_tax 

    return dict(subtotal=subtotal,tax_dict=tax_dict, grand_total=grand_total) #type:ignore
