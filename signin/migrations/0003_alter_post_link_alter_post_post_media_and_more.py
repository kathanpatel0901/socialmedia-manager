# Generated by Django 4.2.9 on 2024-05-10 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signin', '0002_post_post_schedule_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='signin.link'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_media',
            field=models.FileField(blank=True, max_length=10485760, null=True, upload_to='post_media/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
