# Generated by Django 3.2.3 on 2021-06-17 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_alter_channel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
