from celery import shared_task
from tweepy.client import Client
import tweepy


@shared_task
def schedule_post_task(content, social_media):

    # Initialize Tweepy client with your Twitter authentication keys
    twitter_auth_keys = {
        "consumer_key": "ULYeOm844iifGFuE32YyLnzT0",
        "consumer_secret": "xQ9YJjXLDmIjf67e6ZGrxxrhZxg4pyFlnV6qbLYEMEfrbavxDb",
        "access_token": "1758379615968514048-7fCJHGXHwU52KMAS2p1HMOQCjlIymx",
        "access_token_secret": "95eCaWA79LD48G8PgT2pzFAb6CGIqURA9hXm6y1OrUmvJ",
    }

    client = tweepy.Client(
        consumer_key=twitter_auth_keys["consumer_key"],
        consumer_secret=twitter_auth_keys["consumer_secret"],
        access_token=twitter_auth_keys["access_token"],
        access_token_secret=twitter_auth_keys["access_token_secret"],
    )

    # Check if the scheduled post is for Twitter
    if social_media == "Twitter":
        # Post the content to Twitter using the Tweepy client
        client.create_tweet(text=content)
