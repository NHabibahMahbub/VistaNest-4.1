# Generated by Django 5.0.4 on 2025-04-08 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0018_alter_platform_image_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='sold_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='platform',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('sold', 'Sold Out')], default='available', max_length=10),
        ),
    ]
