from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from .forms import UserForm
from .models import User
from django.contrib import messages


def registerUser(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            # create user using form
            # password=form.cleaned_data['password']  #request.POST.get('password')
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.set_password(password)
            # user.save()
            # return redirect(registerUser)

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
            messages.warning(request,'Invalid Information')
            print("Invalid Form")
            print(form.errors)
    else:
        form = UserForm()

    context = {
        'form':form
    }
    return render(request, 'accounts/registerUser.html', context)


