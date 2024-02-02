# twitter_adapter.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class TwitterSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        return 'dashboard/post.html'  # Change this URL as needed
