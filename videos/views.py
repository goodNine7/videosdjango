from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from .forms import EditChannelForm
from videos.models import Channel, Playlist, VideoComment, VideoFiles, VideoDetail, Category, ViewCount
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages import get_messages
from moviepy.editor import VideoFileClip
from datetime import timedelta
import math
from django.urls import reverse

# Create your views here.
def home(request):
    allvideos = VideoFiles.objects.all()
    allvideos = allvideos.filter(video_detail__visibility=True)
    try:
        current_user = request.user
        try:
            channel = Channel.objects.get(user=current_user.id)
        except:
            Channel.objects.get_or_create(
                name=current_user.username, user=current_user, slug=current_user.username)
            channel = Channel.objects.get(user=current_user.id)
        context = {
            'channel': channel,
            'top_nav': channel,
            'videos': allvideos,
            'categories': Category.objects.all()
        }
    except:
        context = {
            'videos': allvideos,
            'categories': Category.objects.all()

        }
    return render(request, 'base.html', context)

def channel(request, slug):
    try:
        videos = VideoFiles.objects.all()
        channel = Channel.objects.get(slug=slug)
        if request.user.id:
            current_user = request.user
            mychannel = Channel.objects.get(user=current_user.id)
            if slug == current_user.username:
                videos = videos.filter(channel__slug=slug)
                context = {
                    'channel': channel,
                    'mychannel': mychannel,
                    'top_nav': mychannel,
                    'videos': videos,
                    'categories': Category.objects.all()
                }
            else:
                videos = videos.filter(channel__slug=slug, video_detail__visibility=True)
                context = {
                    'channel': channel,
                    'mychannel': '',
                    'top_nav': mychannel,
                    'videos': videos,
                    'categories': Category.objects.all()
                }
        else:
            videos = videos.filter(channel__slug=slug, video_detail__visibility=True)
            context = {
                'channel': channel,
                'mychannel': '',
                'top_nav': '',
                'videos': videos,
                'categories': Category.objects.all()
            }
        return render(request, 'channel.html', context)
    except:
        return redirect('index')

def channel_edit(request, slug):
    if request.user.username == slug:
        mychannel = Channel.objects.get(slug=slug)
        if request.method == "POST":
            new_name = request.POST['name']
            if Channel.objects.filter(name=new_name).exists():
                if mychannel.name == new_name:
                    form = EditChannelForm(
                        request.POST, request.FILES, instance=mychannel)
                    if form.is_valid():
                        form.save()
                    context = {
                        'success_message': 'The information was updated successfully.',
                        'channel': mychannel,
                        'mychannel': mychannel,
                        'top_nav': mychannel,
                        'categories': Category.objects.all()
                    }
                    # return render('channel', slug=request.user)
                else:
                    context = {
                        'error_message': 'Channel "{0}" already exists !'.format(new_name),
                        'channel': mychannel,
                        'mychannel': mychannel,
                        'top_nav': mychannel,
                        'categories': Category.objects.all()
                    }
            else:
                form = EditChannelForm(
                    request.POST, request.FILES, instance=mychannel)
                if form.is_valid():
                    form.save()
                context = {
                    'success_message': 'The information was updated successfully.',
                    'channel': mychannel,
                    'mychannel': mychannel,
                    'top_nav': mychannel,
                    'categories': Category.objects.all()
                }
                # return redirect('channel', slug=request.user)
        else:
            form = EditChannelForm(instance=mychannel)
            context = {
                'edit_form': form,
                'channel': mychannel,
                'mychannel': mychannel,
                'top_nav': mychannel,
                'categories': Category.objects.all()
            }
        return render(request, 'channel_edit.html', context)
    else:
        return redirect('index')

@login_required
def upload_video(request):
    messages=''
    if(list(get_messages(request))):
        messages=list(get_messages(request))[0]
        if(str(messages) != "You have successfully uploaded a video"):
            messages=''
    channel = Channel.objects.get(user=request.user.id)
    context = {
        'channel': channel,
        'mychannel': channel,
        'top_nav': channel,
        'success_message': messages,
        'categories': Category.objects.all()
    }
    return render(request, 'file_upload.html', context)

def upload_processing(request):
    channel = Channel.objects.get(slug=request.user.username)
    # category = list(Category.objects.all())
    category = list(Category.objects.values_list('id', 'name'))
    flag = []
    for x in category:
        flag.append({'id': str(x).split(",")[0].strip().split("(")[1].strip(
        ), 'nameCategory': str(x).split(',')[1].strip().replace("'", "").replace(')', '')})
    category = flag
    if channel is not None:
        if request.method == "POST":
            file = request.FILES['file']
            upload = VideoFiles.objects.create(video=file, channel=channel)
            data = {
                'video_id': upload.id,
                'video_path': upload.video.url,
                'category': category
            }
            return JsonResponse(data, safe=False)

        return JsonResponse({'error': 'an error occured'})
    else:
        return redirect('index')

def video_info_process(request):
    if request.method == "POST":
        file_id = request.POST['videofile']
        title = request.POST['title']
        desc = request.POST['description']
        category = Category.objects.get(pk=request.POST['category'])
        visibility = request.POST['visibility']
        thumbnail = request.FILES['thumbnail']
        videofile = get_object_or_404(VideoFiles, id=file_id)
        video_url = "http://localhost:8000{}".format(videofile.video.url)
        video_duration = timedelta(seconds=math.floor(VideoFileClip(video_url).duration))
        VideoDetail.objects.create(
            videofile=videofile, title=title, description=desc, category=category, visibility=visibility, thumbnail=thumbnail, durations=video_duration)
        # messages.add_message(request, messages.INFO, "You have successfully uploaded a video")
        messages.success(request, "You have successfully uploaded a video")
        return redirect('upload_video')
    return redirect('upload_video')

def video_watch_view(request, video_id):
    try:
        video=get_object_or_404(VideoFiles, id=video_id)
        video_cat=video.video_detail.category.name
        suggested_video=VideoFiles.objects.filter(video_detail__category__name=video_cat).exclude(id=video_id)
        ip=request.META['REMOTE_ADDR']
        if not request.session.exists(request.session.session_key):
            request.session.create() 
        if not ViewCount.objects.filter(video=video, session=request.session.session_key):
            view=ViewCount(video=video, ip_address=ip, session=request.session.session_key)
            view.save()
        video_views=ViewCount.objects.filter(video=video).count
        try:
            playlist=get_object_or_404(Playlist, channel=Channel.objects.get(slug=request.user))
        except:
            playlist=''
        context={
            "my_video": video,
            "view_count": video_views,
            "playlist": playlist,
            "recommend_videos":suggested_video,
            'categories': Category.objects.all()
        }
        return render(request, 'watch.html', context)
    except:
        return redirect('index')

def liked_video(request, id):
    user=request.user
    Like=False
    if not request.user.is_authenticated:
        current_url=request.get_full_path()
        login_url=reverse("account_login")
        login_required="{}?next={}".format(login_url, current_url)
        data={
            'login_required':login_required
        }
        return JsonResponse(data, safe=False)
    if request.method=="POST":
        video_id=request.POST['video_id']
        get_video=get_object_or_404(VideoFiles, id=video_id)
        if user in get_video.like.all():
            get_video.like.remove(user)
            Like=False
        else:
            get_video.dislike.remove(user)
            get_video.like.add(user)
            Like=True
        data={
            "liked":Like,
            "like_count": get_video.like.all().count(),
            "dislike_count": get_video.dislike.all().count(),
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse("video_watch", args=[str(id)]))

def disliked_video(request, id):
    user=request.user
    Dislike=False
    if not request.user.is_authenticated:
        current_url=request.get_full_path()
        login_url=reverse("account_login")
        login_required="{}?next={}".format(login_url, current_url)
        data={
            'login_required':login_required
        }
        return JsonResponse(data, safe=False)
    if request.method=="POST":
        video_id=request.POST['video_id']
        get_video=get_object_or_404(VideoFiles, id=video_id)
        if user in get_video.dislike.all():
            get_video.dislike.remove(user)
            Dislike=False
        else:
            get_video.like.remove(user)
            get_video.dislike.add(user)
            Dislike=True
        data={
            "disliked":Dislike,
            "dislike_count": get_video.dislike.all().count(),
            "like_count": get_video.like.all().count(),
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse("video_watch", args=[str(id)]))

def subcriber_view(request, id):
    subcriber=request.user
    Subcribed=False
    if not request.user.is_authenticated:
        current_url=request.get_full_path()
        login_url=reverse("account_login")
        login_required="{}?next={}".format(login_url, current_url)
        data={
            'login_required':login_required
        }
        return JsonResponse(data, safe=False)
    if request.method=="POST":
        channel_id=request.POST['channel_id']
        channel=get_object_or_404(Channel, id=channel_id)
        if subcriber in channel.subcribers.all():
            channel.subcribers.remove(subcriber)
            Subcribed=False
        else:
            channel.subcribers.add(subcriber)
            Subcribed=True
        data={
            'Subcribed':Subcribed,
            'subcriber':channel.num_subcribers()
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse("video_watch", args=[str(id)]))

def addtoplaylist_view(request, id):
    Added=False
    if not request.user.is_authenticated:
        current_url=request.get_full_path()
        login_url=reverse("account_login")
        login_required="{}?next={}".format(login_url, current_url)
        data={
            'login_required':login_required
        }
        return JsonResponse(data, safe=False)
    if request.method=="POST":
        channel=Channel.objects.get(slug=request.user)
        video_id=request.POST['video_id']
        videos=VideoFiles.objects.get(id=video_id)
        try:
            playlist=get_object_or_404(Playlist, channel=channel)
        except:
            Playlist.objects.create(name=request.user, channel=channel, visibility=True)
            playlist=get_object_or_404(Playlist, channel=channel)
        if videos in playlist.video.all():
            playlist.video.remove(videos)
            Added=False
        else:
            playlist.video.add(videos)
            Added=True
        data={
            "added":Added,
            "playlist":playlist.video.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse("video_watch", args=[str(id)]))

def video_comment(request, id):
    if not request.user.is_authenticated:
        current_url=request.get_full_path()
        login_url=reverse("account_login")
        login_required="{}?next={}".format(login_url, current_url)
        data={
            'login_required':login_required
        }
        return JsonResponse(data, safe=False)
    if request.method=="POST":
        comment=request.POST['comment']
        video_id=request.POST['video_id']
        video=VideoFiles.objects.get(id=video_id)
        if comment is not None:
            create_comment=VideoComment(video=video, channel=Channel.objects.get(slug=request.user), comment=comment)
            create_comment.save()
        channel_name=Channel.objects.get(slug=request.user)
        channel_avatar=channel_name.avatar.url
        data={
            "total_cmt": video.video_comment.all().count(),
            "channel_name": str(channel_name),
            "channel_avatar": str(channel_avatar),
            "channel_slug":str(request.user)
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse("video_watch", args=[str(id)]))

def video_show(request):
    categories=Category.objects.all()
    videos=VideoFiles.objects.all()
    context={
        'categories': categories,
        'videos':videos
    }
    return render(request, 'videos_show.html', context)

def video_show_by_cat(request, category_name):
    if category_name=="All":
        return redirect(video_show)
    else:
        categories=Category.objects.all()
        category=Category.objects.get(name=category_name)
        videos=VideoFiles.objects.filter(video_detail__category=category)
        context={
            'categories':categories,
            'category_name':category_name,
            'videos':videos
        }
        return render(request, 'videos_show_by_cat.html', context)

def search_rs(request):
    if request.method=='POST':
        videos=VideoFiles.objects.filter(video_detail__title__icontains=request.POST['search'])
        channel_search=Channel.objects.filter(name__icontains=request.POST['search'])
        context={
            'videos':videos,
            'channel_search':channel_search,
            'categories':Category.objects.all(),
            'search_rs': request.POST['search']
        }
    return render(request, 'search_rs.html', context)