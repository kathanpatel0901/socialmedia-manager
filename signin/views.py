from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout

def home(request):
    return render(request, "dashboard/home.html")


# def logout_view(request):
#     logout(request)

def index(request):
    if request.user.is_authenticated:
        return render(request,'dashboard/home.html')
    else:
        return render(request, 'account/index.html')


def login(request):
    return render(request, 'account/login.html')

def social_accounts(request):
    return render(request,'dashboard/social_accounts.html')
