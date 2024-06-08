from signin.models import Post
from celery import shared_task
from datetime import datetime, timedelta
from signin.utils import (
    create_twitter_post,
    create_facebook_post,
    create_instagram_post,
)
from .models import Link, Facebookuser


@shared_task
def my_periodic_task():
    for post_data in Post.objects.all():
        current_datetime = datetime.now().strftime("%d-%m-%y %H:%M")
        local_time = post_data.post_schedule_datetime + timedelta(hours=5, minutes=30)
        post_schedule_datetime = local_time.strftime("%d-%m-%y %H:%M")
        print(post_schedule_datetime, current_datetime)
        if post_schedule_datetime == current_datetime:
            print("time matched sucsess")
            if post_data.link:
                link_instance = Link.objects.filter(id=post_data.link.id).first()
                create_twitter_post(
                    link_instance.access_token,
                    link_instance.access_token_secret,
                    post_data.post_text,
                )
            if post_data.facebook:
                facebookuser_instance = Facebookuser.objects.filter(
                    id=post_data.meta_connection.id
                ).first()
                create_facebook_post(
                    facebookuser_instance.page_access_token,
                    post_data.image,
                    post_data.post_text,
                )
            if post_data.instagram and post_data.image:
                facebookuser_instance = Facebookuser.objects.filter(
                    id=post_data.meta_connection.id
                ).first()
                create_instagram_post(
                    facebookuser_instance.page_access_token,
                    post_data.image,
                    post_data.post_text,
                )
