# Generated by Django 3.2.3 on 2021-07-19 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0022_channel_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='visibility',
            field=models.BooleanField(choices=[(False, 'private'), (True, 'public')], default=True),
            preserve_default=False,
        ),
    ]
