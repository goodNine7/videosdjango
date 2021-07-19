import uuid
from django.db import models
from django.conf import settings
import os
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse
import math



def remove_duplicate_path(fullname):
    fullpathname = os.path.join(settings.MEDIA_ROOT, fullname)
    if os.path.exists(fullpathname):
        try:
            os.remove(fullpathname)
        except:
            next


def channel_directory_path(instance, filename):
    fullname = "video_files/channel_id_{0}/{1}".format(
        instance.channel.id, filename.replace(' ', '_'))
    remove_duplicate_path(fullname)
    return fullname


def avatar_directory_path(instance, filename):
    fullname = "avatar/user_id_{0}/{1}".format(
        instance.user.id, filename.replace(' ', '_'))
    remove_duplicate_path(fullname)
    return fullname


def thumbnail_directory_path(instance, filename):
    fullname = "video_thumbnail/video_id_{0}/{1}".format(
        instance.videofile.id, filename.replace(' ', '_'))
    remove_duplicate_path(fullname)
    return fullname


User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=avatar_directory_path, default='default_avatar.jpg')
    slug = models.SlugField()
    description = models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    subcribers=models.ManyToManyField(User, related_name='subcribers')

    def __str__(self):
        return self.name

    def num_subcribers(self):
        return self.subcribers.count()

class VideoFiles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.FileField(upload_to=channel_directory_path)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="channel_video")
    uploaded = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name="video_loved")
    dislike = models.ManyToManyField(User, related_name="video_disliked")
   
    def __str__(self):
        return f"video_file_{self.id}"

    def get_absolute_url(self):
        return reverse('video_watch', args=[str(self.id)])

    def num_like(self):
        return self.like.count()

    def num_dislike(self):
        return self.dislike.count()

    def favorite_percent(self):
        try:
            favorite=math.floor((float(100)/(self.like.count()+self.dislike.count()))*self.like.count())
        except:
            favorite="0"
        return favorite

class Playlist(models.Model):
    name=models.CharField(max_length=100)
    channel=models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="channel_playlist")
    video=models.ManyToManyField(VideoFiles, related_name="video_playlist")
    visibility = models.BooleanField(choices=((False, "private"), (True, "public")))
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class VideoDetail(models.Model):
    videofile = models.OneToOneField(VideoFiles, on_delete=models.CASCADE, related_name="video_detail")
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    visibility = models.BooleanField(
        choices=((False, "private"), (True, "public")))
    thumbnail = models.ImageField(upload_to=thumbnail_directory_path)
    durations = models.CharField(max_length=50, editable=False)

    def __str__(self):
        return self.title

class ViewCount(models.Model):
    video=models.ForeignKey(VideoFiles, on_delete=models.CASCADE, related_name='view_count')
    ip_address=models.CharField(max_length=50)
    session=models.CharField(max_length=50)

    def __str__(self):
        return self.ip_address

class VideoComment(models.Model):
    video=models.ForeignKey(VideoFiles, on_delete=models.CASCADE, related_name='video_comment')
    channel=models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="channel_comment")
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.channel.name}: {self.comment[:(int(len(self.comment)/int(2)))]}"
