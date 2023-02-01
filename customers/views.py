from django.shortcuts import render,HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages
from orders.models import Order, OrderedFood

# Create your views here.

@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES ,instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile Updated!')
            return redirect(cprofile)
        else:
            messages.error(request,'Something went wrong!!!')
            return redirect(cprofile)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
    context = {
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render(request,'customers/cprofile.html',context)

def my_orders(request):
    if request.GET.get('q') and request.GET.get('q') != 'All':
        # sort order as per search criteria
        order = Order.objects.filter(user=request.user,is_ordered=True,status=request.GET.get('q')).order_by('-created_at')
        q = request.GET.get('q')
    else:
        # Get all orders, without sorting
        order = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
        q="All"
    context ={
        'orders':order,
        'q':q,
    }
    return render(request,'customers/my_orders.html',context)

def order_detail(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number,user=request.user)
        ordered_food = OrderedFood.objects.filter(order=order)

        # find subtotal,tax,total to show in order complete page
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price*item.quantity)
        tax_dict = order.tax_data

        context = {
            'order':order,
            'ordered_food':ordered_food,
            'tax_dict':tax_dict,
            'subtotal':subtotal,
        }
        return render(request,'customers/order_detail.html',context)
    except:
        return redirect('customer')