# Generated by Django 3.2.3 on 2021-08-10 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0024_reportchannel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='subcribers',
            field=models.ManyToManyField(blank=True, related_name='subcribers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ReportVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporter', models.CharField(max_length=20)),
                ('report_reason', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_video', to='videos.videofiles')),
            ],
        ),
    ]
