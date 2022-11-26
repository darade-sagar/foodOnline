from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from .forms import UserForm
from .models import User, UserProfile
from vendor.forms import VendorForm
from accounts.utils import detectUser, send_verification_email

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .customDecorator import check_role_vendor,check_role_customer

# to activate user
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already Logged In!')
        return redirect(myAccount)
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

            # send verification mail
            mail_subject = 'Please activate your account | foodOnline'
            template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject=mail_subject, template=template)


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
    if request.user.is_authenticated:
        messages.warning(request,'You are already Logged In!')
        return redirect(myAccount)
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

            # send verification mail
            mail_subject = 'Please activate your account | foodOnline'
            template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject=mail_subject, template=template)

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
    if request.user.is_authenticated:
        messages.warning(request,'You are already Logged In!')
        return redirect(myAccount)
    if request.POST:
        email = request.POST['email'] 
        password = request.POST['password'] 
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are now logged in!")
            return redirect(myAccount)
        else:
            messages.error(request,"Invalid Creadentials")
            return redirect(login_view)

    else:
        return render(request,'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You are logged out.")
    return redirect(login_view)

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user= None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect(myAccount)
    else:
        messages.error(request,'Invalid Activation link')
        return redirect(myAccount)

def forgot_password(request):
    if request.POST:
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password
            mail_subject = 'Reset your password! | foodOnline'
            template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject=mail_subject, template=template)
            messages.success(request, 'Forgot password link has been sent on your email')
            return redirect(login_view)
        else:
            messages.error(request, 'Account does not exists')
            return redirect(forgot_password)
    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user= None
    return render(request,'accounts/reset_password_validate.html')

def reset_password(request):
    return render(request,'accounts/reset_password.html')