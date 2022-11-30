from django.shortcuts import render, get_object_or_404, redirect

# User import
from vendor.forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from vendor.models import Vendor
from accounts.customDecorator import check_role_vendor
from menu.models import Category, FoodItem

from menu.forms import CategoryForm, FoodItemForm


# package import
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.POST:
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings updated!')
            return redirect(vprofile)
        else:
            print(profile_form.errors)
            print(vendor_form.errors)

    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form' : profile_form,
        'vendor_form' : vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/vprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories':categories,
    }
    return render(request,'vendor/menu-builder.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category_name=category)
    print(fooditems)
    context = {
        'fooditems': fooditems,
        'category' : category,
    }

    return render(request, 'vendor/fooditems_by_category.html',context)

def add_category(request):
    if request.POST:
        print("POST")
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)

            # to ensure we have unique slug
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Category Added Successfully!')
            return redirect(menu_builder)
            
        else:
            messages.error(request,'Validation error!')
            return redirect(add_category)
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html',context)

def edit_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.POST:
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Category Added Successfully!')
            return redirect(menu_builder)
        else:
            messages.error(request,'Validation error!')
            return redirect(add_category)
            

    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category':category
    }
    return render(request,'vendor/edit_category.html',context)

def delete_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted successfuly!')
    return redirect(menu_builder)









# Food CRUD
def add_food(request):
    if request.POST:
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)

            # to ensure we have unique slug
            food.slug = slugify(food_title)
            form.save()
            messages.success(request,'Food Item Added Successfully!')
            return redirect(fooditems_by_category, food.category_name.id)
            
        else:
            messages.error(request,'Validation error!')
            return redirect(add_food)
    else:
        form = FoodItemForm()

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_food.html',context)
