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
    context = {
        'fooditems': fooditems,
        'category' : category,
    }

    return render(request, 'vendor/fooditems_by_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.POST:
        print("POST")
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category_form = form.save(commit=False)
            category_form.vendor = get_vendor(request)

            # to ensure we have unique slug
            category_form.slug = slugify(category_name)
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

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.POST:
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category_form = form.save(commit=False)
            category_form.vendor = get_vendor(request)
            category_form.slug = slugify(category_name)
            category_form.save()
            messages.success(request,'Category Updated Successfully!')
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

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted successfuly!')
    return redirect(menu_builder)









# Food CRUD
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.POST:
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food_form = form.save(commit=False)
            food_form.vendor = get_vendor(request)

            # to ensure we have unique slug
            food_form.slug = slugify(food_title)
            food_form.save()
            messages.success(request,'Food Item Added Successfully!')
            return redirect(fooditems_by_category, food_form.category_name.id)
            
        else:
            messages.error(request,'Validation error!')
            return redirect(add_food)
    else:
        form = FoodItemForm()
        # modify form
        form.fields['category_name'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_food.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request,pk=None):
    food = get_object_or_404(FoodItem,pk=pk)
    if request.POST:
        form = FoodItemForm(request.POST,instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food_form = form.save(commit=False)
            food_form.vendor = get_vendor(request)
            food_form.slug = slugify(food_title)
            food_form.save()
            messages.success(request,'Food Item updated Successfully!')
            return redirect(menu_builder)
        else:
            messages.error(request,'Validation error!')
            return redirect(add_category)
            

    else:
        form = FoodItemForm(instance=food)
        # modify form
        form.fields['category_name'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form': form,
        'food':food
    }
    return render(request,'vendor/edit_food.html',context)


def delete_food(request,pk=None):
    food = get_object_or_404(FoodItem,pk=pk)
    food.delete()
    messages.success(request,'Fod Item has been deleted successfuly!')
    return redirect(fooditems_by_category, food.category_name.id) #type:ignore