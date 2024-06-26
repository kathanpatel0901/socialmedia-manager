# Generated by Django 4.2.9 on 2024-04-30 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0006_alter_socialaccount_extra_data'),
        ('signin', '0002_link_twitter_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='social_media',
        ),
        migrations.AddField(
            model_name='post',
            name='facebook',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='instagram',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='twitter',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Git',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialaccount.socialaccount')),
            ],
        ),
        migrations.CreateModel(
            name='Facebookuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=100)),
                ('page_id', models.IntegerField()),
                ('page_access_token', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialaccount.socialaccount')),
            ],
        ),
    ]
