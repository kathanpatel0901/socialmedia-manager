from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from .forms import PostForm, SchedulePostForm, RepositoryForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .tasks import schedule_post_task
from .models import Link, Facebookuser
from pyfacebook import GraphAPI
import tweepy
from .models import Link, Facebookuser
from linkedin_api import Linkedin
from pyfacebook import GraphAPI
from github import Github


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
    user_instance = SocialAccount.objects.filter(user=request.user).first()
    link_instance = Link.objects.filter(user=user_instance).first()
    twitter_access_token = link_instance.access_token
    twitter_access_token_secret = link_instance.access_token_secret
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret,
    )
    client.create_tweet(text="HEllo twitter this is test ")
    print("Posted to Twitter successfully!")
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

    return render(request, "dashboard/profile1.html")


def google_redirect(request):
    return render(request, "dashboard/home.html")


def twitter_redirect(request):
    return render(request, "account/post.html")


# views.py


def post_success(request):
    return render(request, "dashboard/post_success.html")


CONSUMER_KEY = "gEpUG3sB4Bv7R7nqiq3KxhCvF"
CONSUMER_SECRET = "9I4HGBIQI4ylJag7BNuIRcxsfmOW8SI8r7bM98RLGJ5tqTwhpC"

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
    verifier = request.GET.get("oauth_verifier")
    oauth_token = request.GET.get("oauth_token")
    request_token = AUTH_USER.request_token["oauth_token"]
    request_secret = AUTH_USER.request_token["oauth_token_secret"]

    print("oauth_verifier::", verifier)
    oauth_user = tweepy.OAuth1UserHandler(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        callback="http://127.0.0.1:8000/Taccess",
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

    print("Username::", username)
    print("Userid ::", userid)
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

    return render(request, "dashboard/social_accounts.html")


CLIENT_ID = "bkY4YzlOWmRQVlhmbHczQVBxaUE6MTpjaQ"
CLIENT_SECRET = "mIYHgBwR84rZCXvYQvkJKEu6d1QTJYJEOQQRJjJ-PvX9e1CGqt"
SCOPE = [
    "tweet.read",
    "tweet.write",
]
AUTH = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri="https://socialmediamanager.in.net/taccess2",
    scope=SCOPE,
    client_secret=CLIENT_SECRET,
)


def tauth2(request):
    auth_url = AUTH.get_authorization_url()
    print("authURl::", auth_url)
    return redirect(auth_url)


def taccess2(request):

    AUTH.request_token = {}
    response_url = request.build_absolute_uri()
    print("RESPONSE URL:", response_url)
    access_token = AUTH.fetch_token(
        authorization_response=response_url,
    )
    print("access_token::", access_token)

    response_url = request.build_absolute_uri()
    print("RESPONSE URL:", response_url)
    context = {"response_url": response_url}
    # access_token = AUTH.fetch_token(authorization_response=response_url)
    # print("access_token::", access_token)
    return render(request, "dashboard/social_accounts.html", context)


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
    #     print('client====',client)
    #     response = client.create_tweet(text='hello world')

    #     print(response)
    #     return render(request,'dashboard/post_success.html')

    # return render(request, 'dashboard/tweet.html')


APP_ID = "1869304440238153"
APP_SECRET = "05ebb9ddfc65ab76d6ff98ce56c62cdc"


CONFIG_ID = "1179387696834598"


API = GraphAPI(
    app_id=APP_ID,
    app_secret=APP_SECRET,
    oauth_flow=True,
)
FREDIRECT_URL = "https://socialmediamanager.in.net/facebook_access/"


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
    context = {"access_token": page_access_token}
    return render(request, "dashboard/social_accounts.html", context)


PAGE_ID = "227651403774182"


def facebok_page_access(request):
    dbfb = Facebookuser.objects.get(user="Kathan Patel")
    obj = dbfb.access_token
    access_token = obj.get("access_token")
    page_access_token = API.exchange_page_access_token(
        page_id="227651403774182", access_token=access_token
    )
    api = GraphAPI(app_id=APP_ID, app_secret=APP_SECRET, access_token=page_access_token)
    data = api.post_object(
        object_id=PAGE_ID,
        connection="feed",
        params={
            "fields": "id,message,created_time,from",
        },
        data={"message": "This is a test message by api"},
    )
    context = {"access_token": page_access_token}

    return render(request, "dashboard/social_accounts.html", context)


INSTA_ID = "17841465939257583"


def insta_auth(request):
    dbfb = Facebookuser.objects.get(user="Kathan Patel")
    obj = dbfb.access_token
    access_token = obj.get("access_token")
    api_i = GraphAPI(app_id=APP_ID, app_secret=APP_SECRET, access_token=access_token)
    data = api_i.post_object(
        object_id=INSTA_ID,
        connection="media",
        params={
            "image_url": "https://picsum.photos/200/300",
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


def github_auth(request):
    url = GITAPP.get_login_url(redirect_uri="http://127.0.0.1:8000/github_access")
    return redirect(url)


GITAUTH = Github()
GITAPP = GITAUTH.get_oauth_application(
    client_id="Iv1.720847ca221968b2",
    client_secret="09b5daab4b82a5239a5aeb6526e6606b423fc798",
)
GIT_CLIENT_ID = "Iv1.720847ca221968b2"
GIT_CLIENT_SECRET = "09b5daab4b82a5239a5aeb6526e6606b423fc798"


def github_access(request):
    code = request.GET.get("code")
    if code:
        ntoken = GITAPP.get_access_token(code)
        if ntoken:
            rtoken = ntoken.refresh_token
            token = GITAPP.refresh_access_token(refresh_token=rtoken)
            auth = GITAPP.get_app_user_auth(token=token)
            g = Github(auth=auth)
            user = g.get_user()
            # social_account = request.user.socialaccount_set.first()
            # Git.objects.create(
            #     user=social_account,
            #     username=login,
            #     code=code,
            # )
            print("Token::", user)
            context = {"token": rtoken}
    return render(request, "dashboard/social_accounts.html", context)

    # social_account = request.user.socialaccount_set.first()
    # Git.objects.create(user=social_account, username=login, token=rtoken)
    # if request.method == "POST":
    #     form = RepositoryForm(request.POST)
    #     if "create" in request.POST and form.is_valid():
    #         repo_name = form.cleaned_data["repository_name"]
    #         new_repo = user.create_repo(repo_name)


def gitpost(request):
    form = RepositoryForm(request.POST)
    return render(request, "dashboard/git.html", {"form": form})


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

    #   if request.method == "POST":
    #         form = RepositoryForm(request.POST)
    #         if "create" in request.POST and form.is_valid():
    #             repository_name = form.cleaned_data["repository_name"]
    #             repository_code = form.cleaned_data["repository_code"]
    #             print("repo name :", repository_name)
    #             action = request.POST.get("action")
    #             if action == "create":
    #                 try:
    #                     repo = user.create_repo(repository_name)
    #                     return HttpResponse("Repository created successfully.")
    #                 except Exception as e:
    #                     return HttpResponse("Error Creating repository: " + str(e))
    #             # if action == "clone":
    #             #     try:
    #             #         repoClone = pygit2.clone_repository(repo.git_url, repository_code)
    #             #         return HttpResponse("Repository cloned successfully.")
    #             #     except Exception as e:
    #             #         return HttpResponse("Error Cloning Repository: " + str(e))
    #     else:
    #         form = RepositoryForm()


def post(request):
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
                twitter_access_token = link_instance.access_token
                twitter_access_token_secret = link_instance.access_token_secret
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
                            message += "Successfully Post on twitter"
                        except Exception as e:
                            message += "Failed to post on Twitter"

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
                                    "fields": "id,message,created_time,from",
                                },
                                data={"message": content},
                            )
                            print("Posted to Facebook successfully!")
                        except Exception as e:
                            message += "Failed to post on Facebook"
                            print("Failed to post on Facebook:", str(e))
                    if not (twitter or facebook):
                        message = "Please Select any one socaial media platform"
                else:
                    message = "Posting on selected media is not supported yet."
    except Exception as e:
        message = str(e)
    return render(
        request, "dashboard/post.html", {"form": form, "error_message": message}
    )
