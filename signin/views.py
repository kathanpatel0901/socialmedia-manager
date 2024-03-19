from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import View
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from .forms import PostForm, SchedulePostForm
from .tasks import schedule_post_task
import tweepy
from .models import Link


from linkedin_api import Linkedin


class Linkedin_auth(View):
    def link(self, request):
        l_auth = Linkedin(username="kathan-patel-78973b1a3", password="Kathan@0901")

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
    callback="http://127.0.0.1:8000/Taccess",
)


@login_required
def tauth(request):
    auth_url = AUTH_USER.get_authorization_url()

    print("authURl::", auth_url)
    return redirect(auth_url)


@login_required
def taccess(request):
    auth_url = request.GET.get("oauth_verifier")
    print("oauth_verifier::", auth_url)
    access_tokenn, access_token_secrett = AUTH_USER.get_access_token(verifier=auth_url)
    print("access_token, access_token_secret::", access_tokenn, access_token_secrett)
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=access_tokenn,
        access_token_secret=access_token_secrett,
    )
    user = client.get_me()
    username = user.data.username
    social_account = request.user.socialaccount_set.first()
    print("Username::", user.data.username)
    xy = Link.objects.filter(Twitter_username=username).first()
    if xy:
        print("reapet")
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
            Twitter_username="Kathanpatel0901", social_media="Twitter"
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
