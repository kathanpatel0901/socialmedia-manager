# google_adapter.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class GoogleSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        return 'dashboard/home.html'  # Change this URL as needed
