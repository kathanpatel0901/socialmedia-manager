from pyfacebook import GraphAPI
import tweepy, os
from dotenv import load_dotenv

SERVER_DOMAIN = os.environ.get("SERVER_DOMAIN")
# Twitter
CONSUMER_KEY = "gEpUG3sB4Bv7R7nqiq3KxhCvF"
CONSUMER_SECRET = "9I4HGBIQI4ylJag7BNuIRcxsfmOW8SI8r7bM98RLGJ5tqTwhpC"

AUTH_USER = tweepy.OAuth1UserHandler(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    callback=f"http://127.0.0.1:8000/Taccess",
)


# Facebook
APP_ID = "1869304440238153"
APP_SECRET = "05ebb9ddfc65ab76d6ff98ce56c62cdc"
CONFIG_ID = "1179387696834598"
PAGE_ID = "227651403774182"

API = GraphAPI(
    app_id=APP_ID,
    app_secret=APP_SECRET,
    oauth_flow=True,
)
FREDIRECT_URL = "https://socialmediamanager.in.net/facebook_access/"


# Instagram
INSTA_ID = "17841465939257583"
