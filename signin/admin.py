from django.contrib import admin
from .models import Link, Post, Git, Facebookuser


# Register your models here.
admin.site.register(Link)
admin.site.register(Post)
admin.site.register(Git)
admin.site.register(Facebookuser)
