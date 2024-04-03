from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.views.generic import View
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm, SchedulePostForm
from .tasks import schedule_post_task
import tweepy
from .models import Link
from linkedin_api import Linkedin
from pyfacebook import GraphAPI
from github import Github, Auth

from pyfacebook import FacebookApi

LINKEDIN_ID = "86mlue1q95me5q"
LINKEDIN_SECRET = "RIGzXPJbqnIZdS3f"
REDIRECT_URL = "http://127.0.0.1:8000/social_account"
LINKEDIN_USERNAME = "kathan-patel-78973b1a3"
LINKEDIN_PASSWORD = "Kathan@0901"


def linkedin(request):
    recip = ["shubham-gor-9017b2228", "archan-patel-5a2174194"]
    # l_auth = Linkedin("patelkathan6@gmail.com", "Kathan@0901")
    l_auth = Linkedin("patelkathan6@gmail.com", "Kathan@0901")
    profile = l_auth.get_profile("kathan-patel")
    print("Linkedin_Auth_Url=", profile)
    return render(request, "dashboard/social_accounts.html")


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


CONSUMER_KEY = "DnvvrDTD4Ala5NcMop7fYPlQ2"
CONSUMER_SECRET = "2AlrKAMN0r8J8jmVBR5tZbnBt0MyKyqc9IvpJVPH1jG6G8jZSZ"

AUTH_USER = tweepy.OAuth1UserHandler(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    callback="https://socialmediamanager.in.net/Taccess",
)


@login_required
def tauth(request):
    auth_url = AUTH_USER.get_authorization_url()

    print("authURl::", auth_url)
    return redirect(auth_url)


@login_required
def taccess(request):
    verifier = request.GET.get("oauth_verifier")
    print("oauth_verifier::", verifier)
    access_tokenn, access_token_secrett = AUTH_USER.get_access_token(verifier=verifier)
    print("access_token, access_token_secret::", access_tokenn, access_token_secrett)
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=access_tokenn,
        access_token_secret=access_token_secrett,
    )

    user = client.get_me()
    username = user.data.username
    userid = user.data.id

    print("Username::", username)
    print("Userid ::", userid)
    social_account = request.user.socialaccount_set.first()
    xy = Link.objects.filter(Twitter_username=username).first()
    if xy:
        print("repeat")
    else:
        Link.objects.create(
            user=social_account,
            Twitter_username=username,
            social_media="Twitter",
            access_token=access_tokenn,
            access_token_secret=access_token_secrett,
        )

    return render(request, "dashboard/social_accounts.html")


def post(request):
    error_message = None
    form = PostForm()
    try:
        user = request.user.id
        userna = request.user.username

        print("id::", user)
        print("name::", userna)
        twitter_auth = Link.objects.get(
            Twitter_username="socialmanager09", social_media="Twitter"
        )
        access_token = twitter_auth.access_token
        access_token_secret = twitter_auth.access_token_secret
        print("token secrets::", access_token)
        # twitter_auth_keys = {
        #     "consumer_key": CONSUMER_KEY,
        #     "consumer_secret": CONSUMER_SECRET,
        #     "access_token": ,
        #     "access_token_secret": "jaHVNjuMSAvQ0KwTDs5GsUvdB5hjyaiAftEFt4uDGQ3Xg",
        # }

        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if "post_now" in request.POST and form.is_valid():
                social_media = form.cleaned_data["social_media"]
                if social_media == "Twitter":
                    content = form.cleaned_data["post_text"]
                    client = tweepy.Client(
                        consumer_key=CONSUMER_KEY,
                        consumer_secret=CONSUMER_SECRET,
                        access_token=access_token,
                        access_token_secret=access_token_secret,
                    )
                    print("user_info==", AUTH_USER)
                    client.create_tweet(text=content)
                    user_screen_name = "socialmanager09"

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


CLIENT_ID = "bkY4YzlOWmRQVlhmbHczQVBxaUE6MTpjaQ"
CLIENT_SECRET = "to1M9-wYHJSYYsRo1EkavkQX6p1HAW_T-VAB7i-_aMcfWESomE"
SCOPE = [
    "tweet.read",
    "tweet.write",
]
AUTH = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri="http://127.0.0.1:8000/show-post",
    scope=SCOPE,
    client_secret=CLIENT_SECRET,
)


def viewshow(request):
    return render(request, "dashboard/showpost.html")


def retrivepost(request):
    auth_url = AUTH.get_authorization_url()
    print("url::", auth_url)
    return redirect(auth_url)


def showpost(request):
    response_url = request.get_full_path()
    print("response url::", response_url)
    access_token = AUTH.fetch_token(response_url)
    print("access_token::", access_token)

    return render(request, "dashboard/showpost.html")


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


APP_ID = "739598838303413"
APP_SECRET = "0ac55bfa64593d4c757ce4ff9f25521d"
API = GraphAPI(
    app_id=APP_ID,
    app_secret=APP_SECRET,
    oauth_flow=True,
)
FREDIRECT_URL = "https://socialmediamanager.in.net/facebook_access"


def facebook_auth(request):
    auth_url_tup = API.get_authorization_url(redirect_uri=FREDIRECT_URL)
    auth_url = auth_url_tup[0]
    print("facebook_url::", auth_url)
    # redirect_url = reverse("facebook_access") + f"?response_url={auth_url}"
    return redirect(auth_url)


PAGE_ID = "61557606137208", "61556785282295"


def facebook_access(request):
    response_url = request.build_absolute_uri()
    print("RESPONSE URL:", response_url)
    # print("access_token::", access_token)
    # access_token = API.exchange_user_access_token(
    #     response=response_url, redirect_uri=FREDIRECT_URL
    # )
    # api = GraphAPI(app_id=APP_ID, app_secret=APP_SECRET, access_token=access_token)
    # data = api.post_object(
    #     object_id="61556785282295",
    #     connection="feed",
    #     data={"message": "this is post using social media manager"},
    # )
    # print("facebook post::", data)
    context = {"response_url": response_url}
    return render(request, "dashboard/social_accounts.html", context)


# def facebook_access(request):
def instabasic(request):
    return render(request, "dashboard/social_accounts.html")


def github_auth(request):
    url = "https://github.com/apps/social-app-auth"
    return redirect(url)


GIT_CLIENT_ID = "Iv1.2b28b44755244ce6"
GIT_CLIENT_SECRET = "75783268896ec8d9313e8a7559c9c8f218519ae7"


def github_access(request):
    code = request.GET.get("code")
    print("code ::", code)
    auth = Github()
    app = auth.get_oauth_application(
        "Iv1.2b28b44755244ce6", "75783268896ec8d9313e8a7559c9c8f218519ae7"
    )
    token = app.get_access_token(code)
    print("Token::", token)

    return render(request, "dashboard/social_accounts.html")
