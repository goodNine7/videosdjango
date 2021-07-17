"""videosdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from videos.views import (home, channel,
                          channel_edit,
                          upload_video,
                          upload_processing,
                          video_info_process, video_show_by_cat,
                          video_watch_view,
                          liked_video,
                          disliked_video,
                          subcriber_view,
                          addtoplaylist_view,
                          video_comment,
                          video_show,
                          search_rs
                          )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home, name="index"),
    path('channel/<slug>/', channel, name="channel"),
    path('channel/<slug>/edit', channel_edit, name="channel_edit"),
    path('upload/', upload_video, name="upload_video"),
    path('uploading/', upload_processing, name="processing"),
    path('video_detail/', video_info_process, name="video_data"),
    path('watch/?v=<video_id>', video_watch_view, name="video_watch"),
    path('like/<uuid:id>', liked_video, name="like_video"),
    path('dislike/<id>', disliked_video, name="dislike_video"),
    path('subcribe/<id>', subcriber_view, name='subcriber'),
    path('add_to_playlist/<id>', addtoplaylist_view, name='add_to_playlist'),
    path('comment/<id>', video_comment, name='comment'),
    path('videos_show/', video_show, name='video_show'),
    path('videos_show/?category=<category_name>', video_show_by_cat, name='video_by_cat'),
    path('search/', search_rs, name='search_rs')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
