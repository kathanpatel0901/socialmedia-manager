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
)

urlpatterns = [
    # path("Linkedin/auth/", Linkedin_auth.as_view(), name="Linkedin_auth"),
    path("Twitter", tauth, name="Twitter_auth"),
    path("Taccess", taccess, name="access-token"),
    path("", home),
    # # path('logout', views.logout_view),
    path("index", index),
    # path('social_account', social_accounts),
    path("post", post),
    path("social_account", social_accounts),
    path("profile", profile_view),
    path("post_success", post_success),
    path("test", test),
    path("schedule-post", schedule_post),
    # path('login', login),
    # path('google-redirect/', google_redirect, name='google_redirect'),
    # path('twitter-redirect/', twitter_redirect, name='twitter_redirect'),
]
