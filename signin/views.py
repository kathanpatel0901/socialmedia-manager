from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import View
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.auth.decorators import login_required
from .forms import PostForm, SchedulePostForm
from .tasks import schedule_post_task
import tweepy
from .models import Link
from allauth.socialaccount.views import ConnectionsView
from requests_oauthlib import OAuth2Session
from django.http import Http404


def link(request):
    social_app = SocialApp.objects.get(provider="twitter_oauth2")
    client_id = social_app.client_id
    client_secret = social_app.secret
    print("Client_id:", client_id)
    print("Secret:", client_secret)
    scope = "tweet.read"
    redirect_uri = "http://127.0.0.1:8000/social_account"
    auth = tweepy.OAuth1UserHandler(
        consumer_key=client_id,
        consumer_secret=client_secret,
        callback=redirect_uri,
    )
    print("AUTH_URL", auth.get_authorization_url())
    return render(request, "dashboard/social_accounts.html",{"a":auth_url})

    # return render(request, "dashboard/social_accounts.html")

    # Handle the case where the SocialApp object for Twitter provider does not exist

    # Handle GET requests
    # You can render a template or redirect the user to another page
    # client_id = "bkY4YzlOWmRQVlhmbHczQVBxaUE6MTpjaQ"
    # client_secret = "UD6w6PzOSkG7jYLotKJoNk2jitzgwUYfawC3_IAHNyriseCj_B"
    # if request.method == "POST":
    #     auth = tweepy.OAuth2UserHandler(client_id, client_secret)
    #     api = tweepy.API(auth)
    #     if request.user.is_authenticated:
    #         return render(request, "dashboard/socail_account.html")
    #     else:
    #         return render(request, "account/index.html")


def index(request):
    if request.user.is_authenticated:
        return render(request, "dashboard/home.html")
    else:
        return render(request, "account/index.html")


def home(request):
    #    return render(request, "dashboard/home.html")
    return index(request)


def test(request):
    return render(request, "base/test.html")


def login(request):
    import pdb

    pdb.set_trace()
    print(request.data)
    return render(request, "account/login.html")


def social_accounts(request):
    return render(request, "dashboard/social_accounts.html")


@login_required
def profile_view(request):

    social_account = SocialAccount.objects.get(user=request.user, provider="google")
    print("social_account", social_account)
    profile_data = social_account.extra_data
    print("profile:data", profile_data)
    profile_picture_url = profile_data.get("picture")
    name = profile_data.get("name")
    sname = profile_data.get("given_name")
    email = profile_data.get("email")
    birthday = profile_data.get("birthday")
    gender = profile_data.get("gender")

    user = request.user
    last_login = user.last_login
    date_joined = user.date_joined

    return render(request, "dashboard/profile.html")


def google_redirect(request):
    return render(request, "dashboard/home.html")


def twitter_redirect(request):
    return render(request, "account/post.html")


# views.py


def post_success(request):
    return render(request, "dashboard/post_success.html")


def post(request):
    error_message = None
    form = PostForm()
    try:
        twitter_auth_keys = {
            "consumer_key": "EYbwRSP5iVELsnzXQP5TIeLy9",
            "consumer_secret": "qg0PkaLFBGTGoQkGO5zZCrIAh0yLcUN5dUYdRu1jYNi8IQwmlv",
            "access_token": "1758379615968514048-CJdisV2q46phy9T45BMt23jsP3k0UX",
            "access_token_secret": "6ga5QraENN6dQ5zPwPx3qyJdJdGjdM0IaQiKOhsGwm8fe",
        }

        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if "post_now" in request.POST and form.is_valid():
                social_media = form.cleaned_data["social_media"]
                if social_media == "Twitter":
                    content = form.cleaned_data["post_text"]
                    client = tweepy.Client(
                        consumer_key=twitter_auth_keys["consumer_key"],
                        consumer_secret=twitter_auth_keys["consumer_secret"],
                        access_token=twitter_auth_keys["access_token"],
                        access_token_secret=twitter_auth_keys["access_token_secret"],
                    )
                    client.create_tweet(text=content)
                    return render(request, "dashboard/post_success.html")
                else:
                    error_message = (
                        "Posting to selected social media is not supported yet."
                    )
    except Exception as e:
        error_message = str(e)

    return render(
        request, "dashboard/post.html", {"form": form, "error_message": error_message}
    )


def schedule_post(request):
    error_message = None
    form = SchedulePostForm()
    if request.method == "POST":
        form = SchedulePostForm(request.POST, request.FILES)
        if form.is_valid():
            post_schedule_time = form.cleaned_data["post_schedule_time"]
            content = form.cleaned_data["post_text"]
            social_media = form.cleaned_data["social_media"]

            # Queue Celery task for scheduled post
            schedule_post_task.apply_async(
                args=[content, social_media], eta=post_schedule_time
            )
            return render(request, "dashboard/SchedulePostSuccess.html")

    return render(
        request,
        "dashboard/SchedulePost.html",
        {"form": form, "error_message": error_message},
    )


# TO fetch account data
def my_callback_view(request):
    social_account = SocialAccount.objects.get(user=request.user, provider="google")
    profile_data = social_account.extra_data
    profile_picture_url = profile_data.get("picture")
    name = profile_data.get("name")
    birthday = profile_data.get("birthday")
    gender = profile_data.get("gender")

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
