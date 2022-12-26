from django.shortcuts import render,redirect,HttpResponse
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from .forms import OrderForm
from .models import Order,Payment, OrderedFood
from django.contrib import messages
from .utils import generate_order_number

# Create your views here.
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')

    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['total_tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            # Address
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']

            order.user = request.user
            order.total = grand_total #type:ignore
            order.tax_data = tax_data #type:ignore
            order.total_tax = total_tax #type:ignore
            order.payment_method = request.POST['payment_method']
            order.save() #It will generate id
            order.order_number = generate_order_number(order.id) #type:ignore
            order.save()
            context ={
                'order':order,
                'cart_items':cart_items,
            }
            return render(request,'orders/place-order.html',context)
        else:
            print(form.errors)
    return render(request,'orders/place-order.html')

# function to check if request is AJAX or not
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def payments(request):
    # check if request is Ajax
    if is_ajax(request) and request.method=="POST":

        # Store Payment details in Payment Model
        order_number = request.POST['order_number']
        transaction_id = request.POST['transaction_id']
        payment_method = request.POST['payment_method']
        status = request.POST['status']
        order = Order.objects.get(user=request.user,order_number=order_number)
        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()

        # Update the order model
        order.payment = payment
        order.is_ordered =True
        order.save()

        # move order to old ordered foods model
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price #type:ignore
            ordered_food.amount = item.fooditem.price * item.quantity #type:ignore
            ordered_food.save()
        
        return HttpResponse("Saved Food")


    return HttpResponse("PaymentPage")