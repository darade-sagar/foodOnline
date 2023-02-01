from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from vendor.models import Vendor, OpeningHour
from marketplace.models import Cart
from menu.models import Category, FoodItem
from orders.forms import OrderForm
from django.http import JsonResponse
from .context_processors import get_cart_counter, get_cart_amounts
from accounts.models import UserProfile
from django.db.models import Sum
from django.db.models import Prefetch, Q
from django.contrib.auth.decorators import login_required
from rating.models import Rating
from django.urls import reverse
import math
from datetime import date

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
    context = {}
    # Search the food by category START
    if request.GET.get('category') != None:
        categories = Category.objects.filter(vendor=vendor,category_name=request.GET.get('category')).prefetch_related(
            Prefetch(
                'fooditems',
                queryset= FoodItem.objects.filter(is_available=True)
            )
        )
        context.update({'searched_category':request.GET.get('category')})
    else:
        categories = Category.objects.filter(vendor=vendor).prefetch_related(
            Prefetch(
                'fooditems',
                queryset= FoodItem.objects.filter(is_available=True)
            )
        )
    # Search the food by category Ends

    # All categories present for vendor
    allcategories = Category.objects.filter(vendor=vendor).prefetch_related(
            Prefetch(
                'fooditems',
                queryset= FoodItem.objects.filter(is_available=True)
            )
        )

    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')
    try:
        # Check current day opening hours
        today_date = date.today()
        today = today_date.isoweekday()
        current_opening_hours = OpeningHour.objects.get(vendor=vendor,day=today)
    except:
        current_opening_hours = None
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context.update({
        'vendor' : vendor,
        'categories':categories,
        'cart_items':cart_items,
        'opening_hours':opening_hours,
        'current_opening_hours':current_opening_hours,
        'is_open':vendor.is_open,
        'allcategories':allcategories,
    })
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
                # check if fooditem is present in cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if checkCart.quantity>1:
                        # if count of fooditem > 1, We will reduce count by 1
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        # else we will delete food item from cart
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
                if cart_item: # if food exist in cart, we will delete food
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

def search(request):
    keyword = request.GET['keyword']
    address = request.GET['location']

    # get vendors which has food items the user is looking for
    fetch_vendors_by_food_item = FoodItem.objects.filter(
        Q(food_title__icontains=keyword) | Q(description__icontains=keyword),
        is_available=True,
    ).values_list('vendor',flat=True)
    
    vendors = Vendor.objects.filter(
        Q(id__in=fetch_vendors_by_food_item) |
        Q(vendor_name__icontains=keyword, 
        is_approved=True,
        user__is_active=True,
        user_profile__address__icontains=address,)
    )
    context = {
        'vendors':vendors,
        'vendor_count':vendors.count()
    }
    return render(request,'marketplace/listings.html',context)


@login_required(login_url='login')
def checkout(request):
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name':request.user.first_name.capitalize(),
        'last_name':request.user.last_name.capitalize(),
        'phone':request.user.phone_number,
        'email':request.user.email,
        'address':user_profile.address,
        'country':user_profile.country,
        'state':user_profile.state,
        'city':user_profile.city,
        'pin_code':user_profile.pincode,
    }
    form = OrderForm(initial=default_values)
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect(marketplace)
    context = {
        'form':form,
        'cart_items':cart_items,
    }
    return render(request,'marketplace/checkout.html',context)


def product_info(request,id):
    #vendor other categories
    product = FoodItem.objects.get(id=id)
    vendor = product.vendor
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )[:3]

    # If anyone submit rating, then save it
    if request.POST:
        rate_value = request.POST.get('rate_value')
        comment = request.POST.get('comment')
        fooditem = FoodItem.objects.get(id=id)
        rating, created = Rating.objects.update_or_create(
            food_item=fooditem, user=request.user,
            defaults={'rate_value': rate_value, 'comment': comment}
        )
        return redirect(reverse('product_info', args=[id]))
    
    # get user_rating for current product
    try:
        user_rating = Rating.objects.get(food_item__id = id, user=request.user)
    except:
        user_rating = None

    # Overall Rating
    rating_obj = Rating.objects.filter(food_item__id=id).order_by('-updated_at')
    rating_sum = rating_obj.aggregate(Sum('rate_value'))
    total_ratings = rating_obj.count()

    if total_ratings>0:
        product_rating = math.ceil(rating_sum.get('rate_value__sum', 0)//total_ratings)
    else:
        product_rating = 0

    # all comment/review of product
    comments = [i.comment for i in rating_obj]

    context={
        'product':product, # Product to be showed
        'categories':categories, #vendor other categories
        'user_rating':user_rating, #user rating value
        'product_rating':product_rating, #product rating values
        'total_ratings':total_ratings, #product overall rating
        'rating_obj':rating_obj[:5], # show comment of products
    }
    return render(request,'marketplace/product_info.html',context)