# Generated by Django 5.1.4 on 2024-12-21 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviesseries',
            name='average_rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
    ]
