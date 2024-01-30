from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,)
    is_active = models.BooleanField(default= True)
    is_deleted = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True) 

    class Meta:
        abstract = True

class User(AbstractUser,BaseModel):
    gender_choice=[('Male', 'Male'),('Female','Female'),('Transgender','Transgender'),('Non-Binary','Non-Binary')]
    # user_id = models.CharField(max_length=60, primary_key=True)
    # email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics')
    bio = models.TextField()
    date_of_birth = models.DateField()
    gender = models.CharField(choices=gender_choice)


class SocialMedia(BaseModel):
    social_media = [('Twitter', 'Twitter'), ('Facebook', 'Facebook'), ('Instagram', 'Instagram'), ('Linkedin', 'Linkedin')]
    account_id = models.CharField(max_length=60, primary_key=True)
    account_password = models.CharField(max_length=16)
    social_platforms = models.CharField(choices=social_media)
    access_token = models.TextField()
    refresh_token = models.TextField()
  
class Post(BaseModel):
    post_id = models.IntegerField(max_length=32, primary_key=True)
    account_id = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    post = models.FileField(upload_to='post')
    post_content = models.TextField()
    post_date_time = models.DateTimeField()

