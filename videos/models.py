import uuid
from django.db import models
from django.conf import settings
from django.db.models.base import Model

def channel_directory_path(instance, filename):
    return "video_files/channel_id_{0}/{1}".format(instance.channel.id, filename)

def avatar_directory_path(instance, filename):
    return "avatar/user_id_{0}/{1}".format(instance.user.id, filename)

def thumbnail_directory_path(instance, filename):
    return "video_thumbnail/video_file_{0}/{1}".format(instance.videofile.id, filename)

User=settings.AUTH_USER_MODEL

class Category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Channel(models.Model):
    name=models.CharField(max_length=200)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to=avatar_directory_path, default='default_avatar.jpg')
    slug=models.SlugField()
    description=models.TextField()
    def __str__(self):
        return self.name

class VideoFiles(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video=models.FileField(upload_to=channel_directory_path)
    channel=models.ForeignKey(Channel, on_delete=models.CASCADE)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    uploaded=models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return f"video_file_{self.id}"

class VideoDetail(models.Model):
    videofile=models.OneToOneField(VideoFiles, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField(max_length=200)
    visibility=models.BooleanField(choices=((False, "private"), (True, "public")))
    thumbnail=models.ImageField(upload_to=thumbnail_directory_path)
    def __str__(self):
        return self.title