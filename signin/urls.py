
from django.urls import path
from .import views

urlpatterns = [

    path('home',views.home),
    # # path('logout', views.logout_view),
    path('', views.index),
    
    path('social_account', views.social_accounts)
]