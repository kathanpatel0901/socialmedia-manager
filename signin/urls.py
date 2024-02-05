
from django.urls import path
from signin.views import home,index,post_tweet,social_accounts,profile_view,post_success

urlpatterns = [

    path('home',home),
    # # path('logout', views.logout_view),
    path('index',index),
    
    # path('social_account', social_accounts),
    path('post_view', post_tweet),
    path('social_account', social_accounts),
    path('profile', profile_view),
    path('post_success', post_success),
    # path('login', login),
    # path('google-redirect/', google_redirect, name='google_redirect'),
    # path('twitter-redirect/', twitter_redirect, name='twitter_redirect'),
   
]   