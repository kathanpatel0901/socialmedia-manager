from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

SOCIAL_MEDIA_CHOICES = [
    ("Twitter", "Twitter"),
    ("Facebook", "Facebook"),
    ("Instagram", "Instagram"),
    ("LinkedIn", "LinkedIn"),
    ("Pinterest", "Pinterest"),
]


class Link(models.Model):
    user = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    Twitter_username = models.CharField(max_length=50)
    social_media = models.CharField(max_length=20)
    access_token = models.CharField(max_length=200)
    access_token_secret = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.Twitter_username} - {self.social_media}"


class Post(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    post_text = models.CharField(max_length=100)
    post_media = models.FileField(upload_to="post_media/", max_length=10485760)
    social_media = models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHOICES)
    post_date_time = models.DateTimeField(default=timezone.now)
    post_type = models.CharField(max_length=20)
    post_schedule_time = models.DateTimeField()

    def __str__(self):
        return f"Post {self.id} by {self.user.username} on {self.social_media}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.post_date_time = timezone.now()
        return super().save(*args, **kwargs)

class Git(models.Model):
    user = models.CharField(max_length=100)