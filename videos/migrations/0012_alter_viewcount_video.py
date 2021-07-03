# Generated by Django 3.2.3 on 2021-07-02 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_viewcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewcount',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.videofiles'),
        ),
    ]