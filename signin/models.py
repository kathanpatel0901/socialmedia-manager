from django.db import models
import uuid
from django.utils import timezone

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
    post_media = models.FileField(upload_to='post_media/', max_length=10485760)
    social_media = models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHOICES)    
    post_date_time = models.DateTimeField(default = timezone.now)
    post_type = models.CharField(max_length = 20)
    

    def __str__(self):
        return f"Post {self.id}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.post_date_time = timezone.now()
        return super().save(*args, **kwargs)
        
