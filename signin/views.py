from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views import View
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from .forms import TweetForm
from django.conf import settings
import tweepy
from tweepy.auth import OAuth1UserHandler, OAuth2AppHandler
from tweepy.client import Client, Response



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

def profile_view(request):
   return render(request, 'dashboard/profile.html')


def google_redirect(request):
    return render(request, 'dashboard/home.html')

def twitter_redirect(request):
    return render(request, 'account/post.html')

# views.py
def post_tweet(request):
   return render(request, 'dashboard/post.html' )

def post_success(request):
   return render(request, 'dashboard/post_success.html')

# @login_required
# def post_tweet(request):
#     if request.method == 'POST':
#         form = TweetForm(request.POST)
#         if form.is_valid():
#             tweet_content = form.cleaned_data['tweet_content']

#             auth = tweepy.OAuth1UserHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
#             auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

#             api = tweepy.API(auth)

#             # Post the tweet
#             api.update_status(tweet_content)

#             return redirect('post_success')  # Create a success page or redirect as needed
#     else:
#         form = TweetForm()

#     return render(request, 'dashboard/post.html', {'form': form})



def tweet(request):
    BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAB6AsQEAAAAAKUpf0jySlMJCNFSb%2B73NY%2FwKPyc%3DGRBoKmU6Y8KIsLiRrNboMNqAJ7flBFHuLrNsitBu61G4c4E4dP'
    CONSUMER_KEY = 'Y2hCQXhVVzl0Y0RMWmR2T19XZ3Y6MTpjaQ'
    CONSUMER_SECRATE ='L4Q4EsxJLc5Byw3428sRLbxIVMua8ZdqVDiycUYpB9HpuTKAqM'
    TWITTER_API_KEY = '2PegHCEvjFbsF7mLgJbxQQzks'
    TWITTER_API_SECRET_KEY = 'XsTi5z1MmOZ9tUu8r5yituADNvrnFQmIbzsnqmgUUPfRKwc2hI'
    TWITTER_ACCESS_TOKEN = '1698066183910768640-qVGbLnFiIwvJ7uWKWcXYYp1yjOOzyF'
    TWITTER_ACCESS_TOKEN_SECRET = 'ycObapiXdEf91PQBye23LuoSb1IGDEqAzdqWKQlpxfjyi'

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            print('Content:', content)
        
        
            auth = OAuth2AppHandler(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRATE)
            api = Client(auth)
            test = api.create_tweet(text=content)
            print("==================",test)

            return render(request,'dashboard/post_success.html')

    return render(request, 'dashboard/tweet.html')



    # if request.method == 'POST':
    #   content = request.POST.get('content','')

    #   if content:
    #     client = tweepy.Client(consumer_key=CONSUMER_KEY,
    #                    consumer_secret=CONSUMER_SECRATE,
    #                    access_token=TWITTER_ACCESS_TOKEN,
    #                    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    #     print('client===========',client)
    #     response = client.create_tweet(text='hello world')

    #     print(response)
    #     return render(request,'dashboard/post_success.html')

    # return render(request, 'dashboard/tweet.html')