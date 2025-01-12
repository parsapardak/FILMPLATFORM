# Generated by Django 5.1.4 on 2024-12-21 20:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_actor_moviesseries_genre_movies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='awards',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='director',
            name='nationality',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='moviesseries',
            name='is_series',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='watchlist',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]