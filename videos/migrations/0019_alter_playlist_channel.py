# Generated by Django 3.2.3 on 2021-07-06 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0018_playlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channel_playlist', to='videos.channel'),
        ),
    ]
