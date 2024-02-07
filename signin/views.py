from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views import View
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
import tweepy
from tweepy import OAuthHandler, API
from .forms import TweetForm
from django.conf import settings



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
def post_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet_content = form.cleaned_data['tweet_content']

            auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
            auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

            api = tweepy.API(auth)

            # Post the tweet
            api.update_status(tweet_content)

            return redirect('post_success')  # Create a success page or redirect as needed
    else:
        form = TweetForm()

    return render(request, 'dashboard/post.html', {'form': form})


