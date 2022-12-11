from django.shortcuts import render, get_object_or_404, HttpResponse
from vendor.models import Vendor
from marketplace.models import Cart
from menu.models import Category, FoodItem
from django.http import JsonResponse
from .context_processors import get_cart_counter, get_cart_amounts

from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request,'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context ={
        'vendor' : vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request,'marketplace/vendor_detail.html',context)

# function to check if request is AJAX or not
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def add_to_cart(request,food_id):
    # this function will be called from AJAX request.
    if request.user.is_authenticated:
        if is_ajax(request):
            # check if food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if user has aleady added that food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # inc cart qty
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status':'Success', 'message':'incresed the cart qty','cart_counter':get_cart_counter(request),'qty':checkCart.quantity,'cart_ammount':get_cart_amounts(request)})

                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success', 'message':'Added the food to cart','cart_counter':get_cart_counter(request),'qty':checkCart.quantity,'cart_ammount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'failed', 'message':'this food does not exist'})

        else:
            return JsonResponse({'status':'failed', 'message':'Invalid Request'})
    else:
        return JsonResponse({'status':'Login_Required', 'message':'Please Login to continue'})

def decrease_cart(request, food_id):
    # this function will be called from AJAX request.
    if request.user.is_authenticated:
        if is_ajax(request):
            # check if food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if user has aleady added that food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if checkCart.quantity>1:
                        # dec cart qty
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                    return JsonResponse({'status':'Success','cart_counter':get_cart_counter(request),'qty':checkCart.quantity,'cart_ammount':get_cart_amounts(request)})

                except:
                    return JsonResponse({'status':'Failed', 'message':'You dont have this item in cart'})
            except:
                return JsonResponse({'status':'failed', 'message':'this food does not exist'})

        else:
            return JsonResponse({'status':'failed', 'message':'Invalid Request'})
    else:
        return JsonResponse({'status':'Login_Required', 'message':'Please Login to continue'})

@login_required(login_url='/login') 
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items':cart_items,
    }
    return render(request,'marketplace/cart.html',context)

def delete_cart(request,cart_id=None):
    # this function will be called from AJAX request.
    if request.user.is_authenticated:
        if is_ajax(request):
            # check if food item exists
            try:
                cart_item = Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'success', 'message':'Cart item has been deleted','cart_counter':get_cart_counter(request),'cart_ammount':get_cart_amounts(request)})
                else:
                    return JsonResponse({'status':'failed', 'message':'Cart does not exist'})
            except:
                return JsonResponse({'status':'failed', 'message':'Cart Item does not exist!'})

        else:
            return JsonResponse({'status':'failed', 'message':'Invalid Request'})
    else:
        return JsonResponse({'status':'Login_Required', 'message':'Please Login to continue'})

