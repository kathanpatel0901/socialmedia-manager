
from django.urls import path
from .import views

urlpatterns = [

    path('home',views.home),
    # # path('logout', views.logout_view),
    path('index', views.index),
    
    path('social_account', views.social_accounts),

    path('login', views.login),
    path('google-redirect/', views.google_redirect, name='google_redirect'),
    path('twitter-redirect/', views.twitter_redirect, name='twitter_redirect'),
   
]   