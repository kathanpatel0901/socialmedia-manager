from django.urls import path
from signin.views import (
    home,
    index,
    social_accounts,
    profile_view,
    post_success,
    post,
    test,
    schedule_post,
    tauth,
    taccess,
    linkedin,
    facebook_auth,
    facebook_access,
    github_auth,
    github_access,
    showpost,
    retrivepost,
    viewshow,

    tauth2,
    taccess2,
    gitpost,
    facebok_page_access,

    instabasic,
    tauth2,
    facebok_page_access,
    taccess2,

    insta_auth,
)

urlpatterns = [
    # path("Linkedin/auth/", Linkedin_auth.as_view(), name="Linkedin_auth"),
    path("Twitter", tauth, name="Twitter_auth"),
    path("Taccess", taccess, name="access-token"),
    path("Linkedin_auth", linkedin, name="linkedin"),
    path("facebook_auth/", facebook_auth, name="facebook_auth"),
    path("facebook_access/", facebook_access, name="facebook_access"),
    path("insta_auth", insta_auth, name="insta_auth"),
    path("github_auth", github_auth, name="github"),
    path("github_access", github_access, name="github_access"),
    path("gitpost", gitpost, name="gitpost"),
    path("get-tweets", retrivepost, name="get-tweets"),
    path("show-post", showpost),
    path("viewshow", viewshow),
    path("", home),

    path("page_access", facebok_page_access),

    path("page_access",facebok_page_access),


    path("page_access",facebok_page_access),

    # # path('logout', views.logout_view),
    path("index", index),
    # path('social_account', social_accounts),
    path("post", post),
    path("social_account", social_accounts),
    path("profile", profile_view),
    path("post_success", post_success),
    path("test", test),
    path("schedule-post", schedule_post),
    path("tauth2", tauth2, name="tauth2"),
    path("taccess2", taccess2, name="taccess2"),
    # path('login', login),
    path("tauth2", tauth2, name="tauth2"),
    path("taccess2",taccess2,name="taccess2"),
    # path('google-redirect/', google_redirect, name='google_redirect'),
    # path('twitter-redirect/', twitter_redirect, name='twitter_redirect'),
]
