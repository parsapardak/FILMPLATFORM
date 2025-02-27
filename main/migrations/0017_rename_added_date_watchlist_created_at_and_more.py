# Generated by Django 5.1.4 on 2025-01-23 16:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_moviesseries_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='added_date',
            new_name='created_at',
        ),
        migrations.AlterUniqueTogether(
            name='watchlist',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='movies',
            field=models.ManyToManyField(related_name='in_watchlists', to='main.moviesseries'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='movie',
        ),
    ]
