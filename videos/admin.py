from django.contrib import admin
from .models import Channel, Category, VideoFiles, VideoDetail, Playlist, VideoComment, ReportChannel, ReportVideo

# Register your models here.
admin.site.register(Channel)
admin.site.register(Category)
admin.site.register(VideoFiles)
admin.site.register(VideoDetail)
admin.site.register(Playlist)
admin.site.register(VideoComment)
admin.site.register(ReportChannel)
admin.site.register(ReportVideo)