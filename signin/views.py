from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from .forms import PostForm, SchedulePostForm, RepositoryForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

# from .tasks import schedule_post_task
from .models import Link, Facebookuser
from pyfacebook import GraphAPI
import tweepy
from .models import Link, Facebookuser
from linkedin_api import Linkedin
import os

from .s3_management import s3_image_upload
from base.constant import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    API,
    APP_ID,
    APP_SECRET,
    PAGE_ID,
    AUTH_USER,
    INSTA_ID,
)

# from load_dotenv()
SERVER_DOMAIN = os.environ.get("SERVER_DOMAIN")

LINKEDIN_ID = "86mlue1q95me5q"
LINKEDIN_SECRET = "RIGzXPJbqnIZdS3f"
REDIRECT_URL = f"{SERVER_DOMAIN}/social_account"
LINKEDIN_USERNAME = "kathan-patel-78973b1a3"
LINKEDIN_PASSWORD = "Kathan@0901"


def linkedin(request):
    recip = ["shubham-gor-9017b2228", "archan-patel-5a2174194"]
    # l_auth = Linkedin("patelkathan6@gmail.com", "Kathan@0901")
    l_auth = Linkedin("patelkathan6@gmail.com", "Kathan@0901")
    profile = l_auth.get_profile("kathan-patel")

    return render(request, "dashboard/social_accounts.html")


def index(request):
    if request.user.is_authenticated:
        return render(request, "dashboard/home.html")
    else:
        return render(request, "account/index.html")


def home(request):
    #    return render(request, "dashboard/home.html")
    return index(request)


def login(request):
    import pdb

    pdb.set_trace()

    return render(request, "account/login.html")


def social_accounts(request):
    user_social_account = request.user.socialaccount_set.first()
    link_instance = Link.objects.filter(user=user_social_account).first()
    facebook_instance = Facebookuser.objects.filter(user=user_social_account).first()
    twitter_exists = link_instance.user if link_instance else None
    facebook_exists = facebook_instance.user is not None if facebook_instance else None
    print(twitter_exists)
    print(facebook_exists)
    return render(
        request,
        "dashboard/social_accounts.html",
        {
            "twitter_exists": twitter_exists,
            "facebook_exists": facebook_exists,
            "user_social_account": user_social_account,
        },
    )


@login_required
def profile_view(request):
    social_account = SocialAccount.objects.get(user=request.user, provider="google")

    profile_data = social_account.extra_data

    profile_picture_url = profile_data.get("picture")
    name = profile_data.get("name")
    sname = profile_data.get("given_name")
    email = profile_data.get("email")
    birthday = profile_data.get("birthday")
    gender = profile_data.get("gender")
    user = request.user
    last_login = user.last_login

    date_joined = user.date_joined

    return render(request, "dashboard/profile1.html")


def google_redirect(request):
    return render(request, "dashboard/home.html")


def twitter_redirect(request):
    return render(request, "account/post.html")


# views.py


def post_success(request):
    return render(request, "dashboard/post_success.html")


@login_required
def tauth(request):
    auth_url = AUTH_USER.get_authorization_url()
    print("authURl::", auth_url)
    return redirect(auth_url)


@login_required
def taccess(request):

    verifier = request.GET.get("oauth_verifier")

    access_tokenn, access_token_secrett = AUTH_USER.get_access_token(verifier=verifier)

    oauth_token = request.GET.get("oauth_token")
    request_token = AUTH_USER.request_token["oauth_token"]
    request_secret = AUTH_USER.request_token["oauth_token_secret"]

    print("oauth_verifier::", verifier)
    oauth_user = tweepy.OAuth1UserHandler(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        callback=f"http://127.0.0.1:8000/Taccess",
    )
    oauth_user.request_token = {
        "oauth_token": request_token,
        "oauth_token_secret": request_secret,
    }
    access_tokenn, access_token_secrett = oauth_user.get_access_token(verifier=verifier)
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

    social_account = request.user.socialaccount_set.first()
    user = Link.objects.filter(Twitter_username=username).first()
    if user:
        user.access_token = access_tokenn
        user.access_token_secret = access_token_secrett
        user.save()
        print("Update Token for ", username)
    else:
        Link.objects.create(
            user=social_account,
            Twitter_username=username,
            social_media="Twitter",
            access_token=access_tokenn,
            access_token_secret=access_token_secrett,
        )
    link_instance = Link.objects.filter(user=social_account).first()
    facebook_instance = Facebookuser.objects.filter(user=social_account).first()
    twitter_exists = link_instance.user if link_instance else None
    facebook_exists = facebook_instance.user if facebook_instance else None
    return render(
        request,
        "dashboard/social_accounts.html",
        {
            "twitter_exists": twitter_exists,
            "facebook_exists": facebook_exists,
        },
    )

    # CLIENT_ID = "bkY4YzlOWmRQVlhmbHczQVBxaUE6MTpjaQ"
    # CLIENT_SECRET = "mIYHgBwR84rZCXvYQvkJKEu6d1QTJYJEOQQRJjJ-PvX9e1CGqt"
    # SCOPE = [
    #     "tweet.read",
    #     "tweet.write",
    # ]
    # AUTH = tweepy.OAuth2UserHandler(
    #     client_id=CLIENT_ID,
    #     redirect_uri="https://socialmediamanager.in.net/taccess2",
    #     scope=SCOPE,
    #     client_secret=CLIENT_SECRET,
    # )

    # def taccess2(request):

    AUTH.request_token = {}
    response_url = request.build_absolute_uri()
    print("RESPONSE URL:", response_url)
    access_token = AUTH.fetch_token(
        authorization_response=response_url,
    )
    print("access_token::", access_token)


#     response_url = request.build_absolute_uri()
#     print("RESPONSE URL:", response_url)
#     context = {"response_url": response_url}
#     # access_token = AUTH.fetch_token(authorization_response=response_url)
#     # print("access_token::", access_token)
#     return render(request, "dashboard/social_accounts.html", context)


#     return render(request, "dashboard/showpost.html")


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
    #
    #     print('client====',client)
    #     response = client.create_tweet(text='hello world')

    #
    #     return render(request,'dashboard/post_success.html')

    # return render(request, 'dashboard/tweet.html')


def facebook_auth(request):
    # auth_url_tup = API.get_authorization_url(redirect_uri=FREDIRECT_URL)
    # auth_url = auth_url_tup[0]
    auth_url = "https://www.facebook.com/v19.0/dialog/oauth?client_id=1869304440238153&redirect_uri=https://socialmediamanager.in.net/facebook_access/&state=PyFacebook&config_id=1179387696834598"

    print("facebook_url::", auth_url)
    # redirect_url = reverse("facebook_access") + f"?response_url={auth_url}"
    return redirect(auth_url)


def facebook_access(request):
    response_url = request.build_absolute_uri()
    access_token_dict = API.exchange_user_access_token(response=response_url)
    access_token = access_token_dict.get("access_token")

    api = GraphAPI(access_token=access_token)
    user = api.get_connection("me", "accounts")
    for page in user.get("data", []):
        page_name = page.get("name")
        page_id = page.get("id")
    if access_token:
        page_access_token = API.exchange_page_access_token(
            page_id=page_id, access_token=access_token
        )
    social_account = request.user.socialaccount_set.first()
    Facebookuser.objects.create(
        user=social_account,
        page_name=page_name,
        page_id=page_id,
        page_access_token=page_access_token,
    )
    print("RESPONSE URL:", response_url)
    link_instance = Link.objects.filter(user=social_account).first()
    facebook_instance = Facebookuser.objects.filter(user=social_account).first()
    twitter_exists = link_instance.user if link_instance else None
    facebook_exists = facebook_instance.user if facebook_instance else None
    return render(
        request,
        "dashboard/social_accounts.html",
        {
            "twitter_exists": twitter_exists,
            "facebook_exists": facebook_exists,
        },
    )


def facebok_page_access(request):
    dbfb = Facebookuser.objects.get(user="Kathan Patel")
    obj = dbfb.access_token
    access_token = obj.get("access_token")
    facebok_page_access_token = API.exchange_page_access_token(
        page_id="227651403774182", access_token=access_token
    )
    api = GraphAPI(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        access_token=facebok_page_access_token,
    )
    data = api.post_object(
        object_id=PAGE_ID,
        connection="feed",
        params={
            "fields": "id,message,created_time,from",
        },
        data={"message": "This is a test message by api"},
    )
    context = {"access_token": facebok_page_access_token}

    return render(request, "dashboard/social_accounts.html", context)


# INSTA_ID = "17841465939257583"


def insta_auth(request):
    user_instance = SocialAccount.objects.filter(user=request.user).first()
    facebook_instance = Facebookuser.objects.filter(user=user_instance).first()
    facebok_page_access_token = facebook_instance.page_access_token
    api_i = GraphAPI(
        app_id=APP_ID, app_secret=APP_SECRET, access_token=facebok_page_access_token
    )
    # image_data = request.FILES.get("media_field")
    # image_url = s3_image_upload(
    #     request=request, image_data=image_data, folder_name="instagram"
    # )
    data = api_i.post_object(
        object_id=INSTA_ID,
        connection="media",
        params={
            "image_url": "https://postinsta.s3.amazonaws.com/hero-4-1.jpg",
            "caption": "Image by socialmedia_manager",
        },
    )
    container_id = data["id"]
    publish_data = api_i.post_object(
        object_id=INSTA_ID,
        connection="media_publish",
        params={
            "creation_id": container_id,
        },
    )
    return render(request, "dashboard/post_success.html")


def instabasic(request):
    return render(request, "dashboard/social_accounts.html")


def post(request):

    message = ""
    form = PostForm()
    try:
        user_instance = SocialAccount.objects.filter(user=request.user).first()
        link_instance = Link.objects.filter(user=user_instance).first()  # twitter
        facebook_instance = Facebookuser.objects.filter(user=user_instance).first()
        twitter_access_token = link_instance.access_token
        twitter_access_token_secret = link_instance.access_token_secret
        link_instance = Link.objects.filter(user=user_instance).first()
        facebook_instance = Facebookuser.objects.filter(user=user_instance).first()

        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                print("Form is Valid")
                content = form.cleaned_data["post_text"]
                twitter = form.cleaned_data.get("twitter")
                facebook = form.cleaned_data.get("facebook")
                instagram = form.cleaned_data.get("instagram")
                twitter_access_token = link_instance.access_token
                twitter_access_token_secret = link_instance.access_token_secret
                facebok_page_access_token = facebook_instance.page_access_token
                api = GraphAPI(
                    app_id=APP_ID,
                    app_secret=APP_SECRET,
                    access_token=facebok_page_access_token,
                )
                image_data = request.FILES.get("post_media")
                print("image_data", image_data)

                image_url = s3_image_upload(
                    request=request,
                    image_data=image_data,
                    folder_name="instagram",
                )
                if "post_now" in request.POST:
                    print("Post Now button clicked")

                    if twitter:
                        print("Twitter switch is ON")

                        try:

                            client = tweepy.Client(
                                consumer_key=CONSUMER_KEY,
                                consumer_secret=CONSUMER_SECRET,
                                access_token=twitter_access_token,
                                access_token_secret=twitter_access_token_secret,
                            )
                            # mapi = tweepy.API(client)
                            # media = mapi.media_upload(image_url)
                            client.create_tweet(text=content)

                        except Exception as e:
                            message += "Failed to post on Twitter"
                    else:
                        message = "please, connect your twitter first"

                    if facebook:
                        print("Facebook switch is ON")
                        try:
                            page_access_token = facebook_instance.page_access_token
                            api = GraphAPI(
                                app_id=APP_ID,
                                app_secret=APP_SECRET,
                                access_token=page_access_token,
                            )
                            data = api.post_object(
                                object_id=PAGE_ID,
                                connection="photos",
                                params={"url": image_url, "caption": content},
                            )
                            print("Posted to Facebook successfully!")
                        except Exception as e:

                            message += "Failed to post on Facebook"
                    else:
                        message = "Please, connect your facebook first"
                else:
                    message = "Posting on selected social media is not supported yet."

                    if not (twitter or facebook):
                        message = "Please Select any one socaial media platform"
    except Exception as e:
        message = str(e)
    return render(
        request, "dashboard/post.html", {"form": form, "error_message": message}
    )


def schedule_post(request):
    message = ""
    form = PostForm()
    print("View function executed")
    try:
        user_instance = SocialAccount.objects.filter(user=request.user).first()
        link_instance = Link.objects.filter(user=user_instance).first()
        facebook_instance = Facebookuser.objects.filter(user=user_instance).first()

        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            print("Form submitted")
            print("Form data:", request.POST)
            if form.is_valid():
                print("Form is Valid")
                content = form.cleaned_data["post_text"]
                twitter = form.cleaned_data.get("twitter")
                facebook = form.cleaned_data.get("facebook")
                post_schedule_date = form.cleaned_data.get("post_schedule_date")
                post_schedule_time = form.cleaned_data.get("post_schedule_time")
                post_schedule_datetime = datetime.combine(
                    post_schedule_date, post_schedule_time
                )
                twitter_access_token = link_instance.access_token
                twitter_access_token_secret = link_instance.access_token_secret
                post_schedule_datetime = timezone.make_aware(post_schedule_datetime)
                if "post_now" in request.POST:
                    print("Post Now button clicked")

                    if twitter:
                        print("Twitter switch is ON")
                        try:
                            client = tweepy.Client(
                                consumer_key=CONSUMER_KEY,
                                consumer_secret=CONSUMER_SECRET,
                                access_token=twitter_access_token,
                                access_token_secret=twitter_access_token_secret,
                            )
                            client.create_tweet(text=content)
                            print("Posted to Twitter successfully!")
                            message += "Successfully Post on twitter \n"
                        except Exception as e:
                            message += "Failed to post on Twitter: {}\n".format(str(e))

                    if facebook:
                        print("Facebook switch is ON")
                        try:
                            page_access_token = facebook_instance.page_access_token
                            api = GraphAPI(
                                app_id=APP_ID,
                                app_secret=APP_SECRET,
                                access_token=page_access_token,
                            )
                            data = api.post_object(
                                object_id=PAGE_ID,
                                connection="feed",
                                params={
                                    "creation_id": container_id,
                                },
                            )
                            message += "Successfully Post on Instagram \n"
                        except Exception as e:
                            message = "Failed to post on instagram{}\n".format(str(e))
                            print(e)

                    if not (twitter or facebook or instagram):
                        message = "Please Select any one socaial media platform\n"
                else:
                    message = "Posting on selected media is not supported yet.\n"
    except Exception as e:
        message = str(e)
    return render(
        request, "dashboard/post.html", {"form": form, "error_message": message}
    )


def schedule_post(request):
    error_message = ""
    form = SchedulePostForm()       
    if request.method == "POST":
        form = SchedulePostForm(request.POST, request.FILES)
        if form.is_valid():
            social_account_instance = SocialAccount.objects.filter(
                user=request.user
            ).first()
            link_instance = Link.objects.filter(user=social_account_instance).first()
            facebook_instance = Facebookuser.objects.filter(
                user=social_account_instance
            ).first()
            print(facebook_instance)

            twitter = form.cleaned_data.get("twitter")
            facebook = form.cleaned_data.get("facebook")
            instagram = form.cleaned_data.get("instagram")
            schedule_post = form.save()
            image_data = request.FILES.get("post_media")
            # if image_data:
            #     image_url = s3_image_upload(
            #         request=request,
            #         image_data=image_data,
            #         folder_name="scheduled-post",
            #     )
            #     print(image_url)
            # schedule_post.image = image_url

            if twitter:
                schedule_post.link = link_instance

            if facebook or instagram:
                schedule_post.meta_connection = facebook_instance

            schedule_post.save()

            return render(request, "dashboard/SchedulePostSuccess.html")

    return render(
        request,
        "dashboard/SchedulePost.html",
        {"form": form, "error_message": error_message},
    )


def schedule_post(request):
    error_message = ""
    form = SchedulePostForm()
    if request.method == "POST":
        form = SchedulePostForm(request.POST, request.FILES)
        if form.is_valid():
            social_account_instance = SocialAccount.objects.filter(
                user=request.user
            ).first()
            link_instance = Link.objects.filter(user=social_account_instance).first()
            facebook_instance = Facebookuser.objects.filter(
                user=social_account_instance
            ).first()
            print(facebook_instance)

            twitter = form.cleaned_data.get("twitter")
            facebook = form.cleaned_data.get("facebook")
            instagram = form.cleaned_data.get("instagram")
            schedule_post = form.save()
            image_data = request.FILES.get("post_media")
            # if image_data:
            #     image_url = s3_image_upload(
            #         request=request,
            #         image_data=image_data,
            #         folder_name="scheduled-post",
            #     )
            #     print(image_url)
            # schedule_post.image = image_url

            if twitter:
                schedule_post.link = link_instance

            if facebook or instagram:
                schedule_post.meta_connection = facebook_instance

            schedule_post.save()

            return render(request, "dashboard/SchedulePostSuccess.html")

    return render(
        request,
        "dashboard/SchedulePost.html",
        {"form": form, "error_message": error_message},
    )
