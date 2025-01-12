# Generated by Django 5.1.4 on 2024-12-21 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_moviesseries_average_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='biography',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='actor',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='actor',
            name='nationality',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]