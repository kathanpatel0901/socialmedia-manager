from django.db import models
import uuid


class Post(models.Model):
    SOCIAL_MEDIA_CHOICES = [
        ('Twitter', 'Twitter'),
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
        ('LinkedIn', 'LinkedIn'),
        ('Pinterest', 'Pinterest'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_text = models.CharField(max_length=100)
    post_media = models.FileField(upload_to='post_media/')
    social_media = models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHOICES)
    post_date_time = models.DateTimeField()

    def __str__(self):
        return f"Post {self.id}"
       
# Create your models here.