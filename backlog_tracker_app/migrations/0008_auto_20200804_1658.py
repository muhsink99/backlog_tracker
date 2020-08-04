# Generated by Django 3.0.3 on 2020-08-04 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backlog_tracker_app', '0007_auto_20200804_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='showbacklog',
            name='current_episode',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='showbacklog',
            name='image_url',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='showbacklog',
            name='max_episodes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='showbacklog',
            name='user_rating',
            field=models.IntegerField(default=0),
        ),
    ]