from django.shortcuts import render, HttpResponse, redirect
from marketplace.models import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    subtotal, tax, total = 0,0,0
    for item in cart_items:
        subtotal += item.fooditem.price*item.quantity
    total += subtotal + tax 

    context = {
        'cart_items':cart_items,
        'total1':total,
        'subtotal1':subtotal,
        'tax1':tax,
    }
    return render(request,'cartApp/cart.html',context)


@login_required(login_url='/login')
def inc_cart(request,id):
    if request.user.is_authenticated:
        fooditem = Cart.objects.filter(user=request.user)
        for food in fooditem:
            if food.id == id: #type:ignore
                food.quantity += 1
                food.save()
                messages.success(request,'Food item added in cart!')
    else:
        messages.warning(request,'User is not authenticated, Please contact Admin!')
    return redirect(cart_page)

@login_required(login_url='/login')
def dec_cart(request,id):
    if request.user.is_authenticated:
        fooditems= Cart.objects.filter(user=request.user)
        for food in fooditems:
            if food.id == id: #type:ignore
                if food.quantity > 1:
                    food.quantity -= 1
                    food.save()
                else:
                    food.delete()
            messages.success(request,'Food item droped from cart!')
    else:
        messages.warning(request,'User is not authenticated, Please contact Admin!')

    return redirect(cart_page)

@login_required(login_url='/login')
def delete_cart(request,id):
    if request.user.is_authenticated:
        food = Cart.objects.filter(user=request.user,id=id)
        food.delete()
        messages.success(request,'Item has been removed!')
    else:
        messages.warning(request,'User is not authenticated, Please contact Admin!')
    return redirect(cart_page)