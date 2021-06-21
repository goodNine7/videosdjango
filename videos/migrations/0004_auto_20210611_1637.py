# Generated by Django 3.2.3 on 2021-06-11 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_alter_videodetail_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='avatar',
            field=models.ImageField(default='default_avatar.jpg', upload_to='channel_avatar/'),
        ),
        migrations.AlterField(
            model_name='videodetail',
            name='thumbnail',
            field=models.ImageField(upload_to=''),
        ),
    ]