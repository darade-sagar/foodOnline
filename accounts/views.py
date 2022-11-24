from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm


def registerUser(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            # create user using create_user method in CustomManager
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username,password=password, email=email)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,'Your account has been register sucessfully')
            return redirect(registerUser)
        else:
            messages.error(request,'Invalid Information')
    else:
        form = UserForm()

    context = {
        'form':form
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.POST:
        form = UserForm(request.POST)
        vform = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vform.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username,password=password, email=email)
            user.role = User.VENDOR
            user.save()

            user_profile = UserProfile.objects.get(user=user)
            vendor = vform.save(commit=False)
            vendor.user = user
            vendor.user_profile = user_profile
            vendor.save()

            messages.success(request,'Your account has been register sucessfully! Please wait for approval')
            return redirect(registerVendor)

        else:
            messages.error(request,'Invalid Form data')

    else:
        
        form = UserForm()
        vform = VendorForm()

    context ={
        'form':form,
        'vform':vform,
    }
    return render(request,'accounts/registerVendor.html', context)


def login_view(request):
    return render(request,'accounts/login.html')

def logout_view(request):
    return render(request,'accounts/logout.html')

def dashboard(request):
    return render(request,'accounts/dashboard.html')