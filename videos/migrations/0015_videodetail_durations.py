# Generated by Django 3.2.3 on 2021-07-02 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0014_alter_videodetail_videofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='videodetail',
            name='durations',
            field=models.CharField(default=0, editable=False, max_length=50),
            preserve_default=False,
        ),
    ]