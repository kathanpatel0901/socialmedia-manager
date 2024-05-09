from celery import shared_task
from tweepy.client import Client
from base.constant import CONSUMER_KEY, CONSUMER_SECRET, APP_ID, APP_SECRET, PAGE_ID
import tweepy
from pyfacebook import GraphAPI


@shared_task
def schedule_post_task(
    content,
    twitter,
    facebook,
    twitter_access_token,
    twitter_access_token_secret,
    # facebok_page_access_token,
):

    print("Twitter switch is ON")

    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret,
    )
    if twitter:
        client.create_tweet(text=content)
        print("Posted to Twitter successfully!")
        return "Successfully  posted on TWitter"

    # if facebook:
    #     print("Facebook switch is ON")
    #     try:
    #         api = GraphAPI(
    #             app_id=APP_ID,
    #             app_secret=APP_SECRET,
    #             access_token=facebok_page_access_token,
    #         )
    #         data = api.post_object(
    #             object_id=PAGE_ID,
    #             connection="feed",
    #             params={
    #                 "fields": "id,message,created_time,from",
    #             },
    #             data={"message": content},
    #         )
    #         print("Posted to Facebook successfully!")
    #     except Exception as e:
    #         message += "Failed to post on Facebook: {}\n".format(str(e))
    # if not (twitter or facebook):
    #     message = "Please Select any one socaial media platform"
    # else:
    #     message = "Posting on selected media is not supported yet."

    # Initialize Tweepy client with your Twitter authentication keys
    # twitter_auth_keys = {
    #     "consumer_key": "ULYeOm844iifGFuE32YyLnzT0",
    #     "consumer_secret": "xQ9YJjXLDmIjf67e6ZGrxxrhZxg4pyFlnV6qbLYEMEfrbavxDb",
    #     "access_token": "1758379615968514048-7fCJHGXHwU52KMAS2p1HMOQCjlIymx",
    #     "access_token_secret": "95eCaWA79LD48G8PgT2pzFAb6CGIqURA9hXm6y1OrUmvJ",
    # }

    # client = tweepy.Client(
    #     consumer_key=twitter_auth_keys["consumer_key"],
    #     consumer_secret=twitter_auth_keys["consumer_secret"],
    #     access_token=twitter_auth_keys["access_token"],
    #     access_token_secret=twitter_auth_keys["access_token_secret"],
    # )

    # # Check if the scheduled post is for Twitter
    # if social_media == "Twitter":
    #     # Post the content to Twitter using the Tweepy client
    #     client.create_tweet(text=content)
