from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views import View
from django.http import HttpResponse


def index(request):
  if request.user.is_authenticated:
    return render(request,'dashboard/home.html')
  else:
      return render(request, 'account/index.html')


def home(request):
#    return render(request, "dashboard/home.html")
 return index(request)




def login(request):
    return render(request, 'account/login.html')
    
def social_accounts(request):
    return render(request,'dashboard/social_accounts.html')




def google_redirect(request):
    return render(request, 'dashboard/home.html')

def twitter_redirect(request):
    return render(request, 'account/post.html')
