# Generated by Django 5.0.4 on 2025-05-06 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0022_userprofile_about_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]
