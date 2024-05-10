import tweepy
from pyfacebook import GraphAPI

from base.constant import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    API,
    APP_ID,
    APP_SECRET,
    PAGE_ID,
    FREDIRECT_URL,
    AUTH_USER,
    INSTA_ID,
)


def create_twitter_post(twitter_access_token, twitter_access_token_secret, content):
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret,
    )
    client.create_tweet(text=content)
    print("test")


def create_facebook_post(facebok_page_access_token, image_url, content):
    api = GraphAPI(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        access_token=facebok_page_access_token,
    )
    params = {}
    if image_url:
        params["url"] = image_url
        params["caption"] = content
        connection_type = "photos"
        api.post_object(object_id=PAGE_ID, connection=connection_type, params=params)
    else:
        connection_type = "feed"
        api.post_object(
            object_id=PAGE_ID,
            connection=connection_type,
            params={"fields": "id,message,craeted_time,from"},
            data={"message": content},
        )


def create_instagram_post(facebok_page_access_token, image_url, content):
    api = GraphAPI(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        access_token=facebok_page_access_token,
    )
    params = {}
    if image_url:
        params["url"] = image_url
    if content:
        params["caption"] = content

    media = api.post_object(
        object_id=INSTA_ID,
        connection="media",
        params=params,
    )
    container_id = media["id"]
    api.post_object(
        object_id=INSTA_ID,
        connection="media_publish",
        params={
            "creation_id": container_id,
        },
    )
