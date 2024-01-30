from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout

# Create your views here.

def home(request):
    return render(request, "dashboard/home.html")

# def logout_view(request):
#     logout(request)
#     return redirect("/")

def index(request):
    return render(request, 'account/index.html')

def social_accounts(request):
    return render(request,'dashboard/social_accounts.html')

