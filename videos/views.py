from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .forms import EditChannelForm
from django.contrib.auth.models import User
from videos.models import Channel, Playlist, ReportChannel, ReportVideo, VideoComment, VideoFiles, VideoDetail, Category, ViewCount
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
    allvideos = allvideos.filter(video_detail__visibility=True, channel__visibility=True).order_by('-uploaded')
    favourite_videos=[]
    for x in allvideos:
        if(int(x.favorite_percent()) > int(60.0)):
            favourite_videos.append(x)
    try:
        current_user = request.user
        try:
            channel = Channel.objects.get(user=current_user.id)
        except:
            Channel.objects.get_or_create(
                name=current_user.username, user=current_user, slug=current_user.username, visibility=True)
            channel = Channel.objects.get(user=current_user.id)
        context = {
            'channel': channel,
            'top_nav': channel,
            'videos': allvideos,
            'favourite_videos': favourite_videos,
            'categories': Category.objects.all()
        }
    except:
        context = {
            'videos': allvideos,
            'favourite_videos': favourite_videos,
            'categories': Category.objects.all()
        }
    return render(request, 'base.html', context)

def channel(request, slug):
    allvideos = VideoFiles.objects.all()
    channel = Channel.objects.get(slug=slug)
    try:
        top_nav=Channel.objects.get(user=request.user.id)
    except:
        top_nav=''
    try:
        videos_in_playlist=allvideos.filter(id__in=Playlist.objects.get(channel=channel, visibility=True).video.all(), video_detail__visibility=True, channel__visibility=True)
        paginator_playlist=Paginator(videos_in_playlist, 6)
        page_number_playlist=request.GET.get('pages')
        page_videos_playlist=paginator_playlist.get_page(page_number_playlist)
    except:
        page_videos_playlist=''
    videos_channel=VideoFiles.objects.filter(channel=channel)
    views_point=int(len(ViewCount.objects.filter(video__in=videos_channel))/int(10))
    if(views_point == int(0)):
        views_point=int(0)
    elif(views_point < int(1)):
        views_point=int(1)
    last_login=User.objects.get(username=slug).last_login
    if request.user.id:
        channel_playlist=Channel.objects.get(user=request.user)
        Playlist.objects.get_or_create(name=request.user.username, channel=channel_playlist, visibility=True)
        current_user = request.user
        mychannel = Channel.objects.get(user=current_user.id)
        if slug == current_user.username:
            videos = allvideos.filter(channel__slug=slug).order_by('-uploaded')
            paginator=Paginator(videos, 6)
            page_number=request.GET.get('page')
            page_videos=paginator.get_page(page_number)
            try:
                videos_in_playlist=allvideos.filter(id__in=Playlist.objects.get(channel=channel).video.all(), video_detail__visibility=True, channel__visibility=True)
                paginator_playlist=Paginator(videos_in_playlist, 6)
                page_number_playlist=request.GET.get('pages')
                page_videos_playlist=paginator_playlist.get_page(page_number_playlist)
            except:
                page_videos_playlist=''
            context = {
                'channel': channel,
                'mychannel': mychannel,
                'top_nav': top_nav,
                'videos': page_videos,
                'categories': Category.objects.all(),
                'last_login': last_login,
                'videos_in_playlist': page_videos_playlist,
                'views_point': views_point
            }
        else:
            videos = allvideos.filter(channel__slug=slug, video_detail__visibility=True).order_by('-uploaded')
            paginator=Paginator(videos, 6)
            page_number=request.GET.get('page')
            page_videos=paginator.get_page(page_number)
            context = {
                'channel': channel,
                'mychannel': '',
                'top_nav': top_nav,
                'videos': page_videos,
                'categories': Category.objects.all(),
                'last_login': last_login,
                'videos_in_playlist': page_videos_playlist,
                'views_point': views_point
            }
    else:
        videos = allvideos.filter(channel__slug=slug, video_detail__visibility=True).order_by('-uploaded')
        paginator=Paginator(videos, 6)
        page_number=request.GET.get('page')
        page_videos=paginator.get_page(page_number)
        context = {
            'channel': channel,
            'mychannel': '',
            'top_nav': '',
            'videos': page_videos,
            'categories': Category.objects.all(),
            'last_login': last_login,
            'videos_in_playlist': page_videos_playlist,
            'views_point': views_point
        }
    return render(request, 'main/channel.html', context)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def channel_edit(request, slug):
    try:
        top_nav=Channel.objects.get(user=request.user.id)
    except:
        top_nav=''
    if request.user.username == slug:
        mychannel = Channel.objects.get(slug=slug)
        if request.method == "POST":
            try:
                if request.POST['username']:
                    if request.POST['pwd1'] == request.POST['pwd2']:
                        if int(len(request.POST['pwd1'])) > int(8.0):
                            user=User.objects.get(username=request.POST['username'])
                            user.set_password(request.POST['pwd1'])
                            user.save()
                            form = EditChannelForm(instance=mychannel)
                            context = {
                                'success_message': 'The User information was updated successfully.',
                                'edit_form': form,
                                'channel': mychannel,
                                'mychannel': mychannel,
                                'top_nav': top_nav,
                                'categories': Category.objects.all()
                            }
                            request.session.flush()
                            return redirect('account_login')
                        else:
                            form = EditChannelForm(instance=mychannel)
                            context = {
                                'error_message': 'This password is too short. It must contain at least 8 characters.',
                                'edit_form': form,
                                'channel': mychannel,
                                'mychannel': mychannel,
                                'top_nav': top_nav,
                                'categories': Category.objects.all()
                            }
                    else:
                        form = EditChannelForm(instance=mychannel)
                        context = {
                            'error_message': 'You must type the same password each time.',
                            'edit_form': form,
                            'channel': mychannel,
                            'mychannel': mychannel,
                            'top_nav': top_nav,
                            'categories': Category.objects.all()
                        }
            except:
                new_name = request.POST['name']
                if Channel.objects.filter(name=new_name).exists():
                    if mychannel.name == new_name:
                        form = EditChannelForm(
                            request.POST, request.FILES, instance=mychannel)
                        if form.is_valid():
                            form.save()
                        top_nav=Channel.objects.get(user=request.user.id)
                        context = {
                            'success_message': 'The information was updated successfully.',
                            'channel': mychannel,
                            'mychannel': mychannel,
                            'top_nav': top_nav,
                            'categories': Category.objects.all()
                        }
                        # return render('channel', slug=request.user)
                    else:
                        context = {
                            'error_message': 'Channel "{0}" already exists !'.format(new_name),
                            'channel': mychannel,
                            'mychannel': mychannel,
                            'top_nav': top_nav,
                            'categories': Category.objects.all()
                        }
                else:
                    form = EditChannelForm(
                        request.POST, request.FILES, instance=mychannel)
                    if form.is_valid():
                        form.save()
                    top_nav=Channel.objects.get(user=request.user.id)
                    context = {
                        'success_message': 'The information was updated successfully.',
                        'channel': mychannel,
                        'mychannel': mychannel,
                        'top_nav': top_nav,
                        'categories': Category.objects.all()
                    }
                    # return redirect('channel', slug=request.user)
        else:
            form = EditChannelForm(instance=mychannel)
            context = {
                'edit_form': form,
                'channel': mychannel,
                'mychannel': mychannel,
                'top_nav': top_nav,
                'categories': Category.objects.all()
            }
        return render(request, 'main/channel_edit.html', context)
    else:
        return redirect('index')

@login_required
def upload_video(request):
    try:
        top_nav=Channel.objects.get(user=request.user.id)
    except:
        top_nav=''
    messages=''
    if(list(get_messages(request))):
        messages=list(get_messages(request))[0]
        if(str(messages) != "You have successfully uploaded a video"):
            messages=''
    channel = Channel.objects.get(user=request.user.id)
    last_login=User.objects.get(username=channel.slug).last_login
    videos_channel=VideoFiles.objects.filter(channel=channel)
    views_point=int(len(ViewCount.objects.filter(video__in=videos_channel))/int(10))
    if(views_point == int(0)):
        views_point=int(0)
    elif(views_point < int(1)):
        views_point=int(1)
    context = {
        'channel': channel,
        'mychannel': channel,
        'top_nav': top_nav,
        'success_message': messages,
        'last_login': last_login,
        'views_point': views_point,
        'categories': Category.objects.all()
    }
    return render(request, 'main/file_upload.html', context)

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
        top_nav=Channel.objects.get(user=request.user.id)
    except:
        top_nav=''
    video=get_object_or_404(VideoFiles, id=video_id, channel__visibility=True)
    video_cat=video.video_detail.category.name
    suggested_video=VideoFiles.objects.filter(video_detail__category__name=video_cat, channel__visibility=True, video_detail__visibility=True).order_by('-uploaded').exclude(id=video_id)
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
        "top_nav": top_nav,
        "view_count": video_views,
        "playlist": playlist,
        "recommend_videos":suggested_video,
        'categories': Category.objects.all()
    }
    return render(request, 'main/watch.html', context)
    

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

def subcriber_view(request, id, template):
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
    if template=="channel":
        return redirect(reverse("channel", args=[str(id)]))
    elif template=="watching":
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
        channel=Channel.objects.get(slug=request.user.username)
        video_id=request.POST['video_id']
        videos=VideoFiles.objects.get(id=video_id)
        try:
            playlist=get_object_or_404(Playlist, channel=channel)
        except:
            Playlist.objects.create(name=request.user.username, channel=channel, visibility=True)
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
        if Channel.objects.get(slug=request.user).visibility == False:
            data={
                'blocked': 'You has been blocked !!!'
            }
        else:
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
                "channel_name": str(channel_name.name),
                "channel_avatar": str(channel_avatar),
                "channel_slug":str(request.user)
            }
        return JsonResponse(data, safe=False)
    return redirect(reverse("video_watch", args=[str(id)]))

def video_show(request):
    # try:
    try:
        top_nav=Channel.objects.get(user=request.user.id)
    except:
        top_nav=''
    if request.GET.get('category'):
        category_name=request.GET['category']
        categories=Category.objects.all()
        category=Category.objects.get(name=category_name)
        videos=VideoFiles.objects.filter(video_detail__category=category, channel__visibility=True, video_detail__visibility=True).order_by('-uploaded')
        paginator=Paginator(videos, 6)
        page_number=request.GET.get('page')
        page_videos=paginator.get_page(page_number)
        context={
            'categories':categories,
            'category_name':category_name,
            'videos':page_videos,
            'top_nav': top_nav
        }
        return render(request, 'main/videos_show_by_cat.html', context)
    elif request.GET.get('favorite'):
        categories=Category.objects.all()
        videos = VideoFiles.objects.all()
        videos = videos.filter(channel__visibility=True, video_detail__visibility=True).order_by('-uploaded')
        favorite_videos = []
        for x in videos:
            if int(x.favorite_percent()) > int(60):
                favorite_videos.append(x)
        paginator=Paginator(favorite_videos, 8)
        page_number=request.GET.get('page')
        page_videos=paginator.get_page(page_number)
        context = {
            'categories':categories,
            'videos': page_videos,
            'top_nav': top_nav
        }
        return render(request, 'main/videos_show_by_favorite.html', context)
    else:
        categories=Category.objects.all()
        videos=VideoFiles.objects.all()
        videos=videos.filter(channel__visibility=True, video_detail__visibility=True).order_by('-uploaded')
        paginator=Paginator(videos, 6)
        page_number=request.GET.get('page')
        page_videos=paginator.get_page(page_number)
        context={
            'categories': categories,
            'category_name': 'All',
            'videos':page_videos,
            'top_nav': top_nav
        }
        return render(request, 'main/videos_show.html', context)
    # except:
    #     return redirect('video_show')

def search_rs(request):
    try:
        top_nav=Channel.objects.get(user=request.user.id)
    except:
        top_nav=''
    if request.method=='GET':
        videos=VideoFiles.objects.filter(video_detail__title__icontains=request.GET['search'], video_detail__visibility=True, channel__visibility=True).order_by('-uploaded')
        channel_search=Channel.objects.filter(name__icontains=request.GET['search'])
        paginator=Paginator(videos, 6)
        page_number=request.GET.get('page')
        page_videos=paginator.get_page(page_number)
        context={
            'videos':page_videos,
            'channel_search':channel_search,
            'categories':Category.objects.all(),
            'search_rs': request.GET['search'],
            'top_nav': top_nav
        }
    return render(request, 'main/search_rs.html', context)

def report_channel(request, slug):
    if not request.user.is_authenticated:
            current_url=request.get_full_path()
            login_url=reverse("account_login")
            login_required="{}?next={}".format(login_url, current_url)
            data={
                'login_required':login_required
            }
            return JsonResponse(data, safe=False)
    if request.method=="POST":
        channel=Channel.objects.get(slug=request.POST['channel'])
        report_reason=request.POST['report_reason']
        if not(len(report_reason)):
            data={
                'text_required': 'Please fill out this field.'
            }
            return JsonResponse(data, safe=False)
        else:
            ReportChannel.objects.get_or_create(channel=channel, reporter=request.user, report_reason=report_reason)
            data={
                'success_mes': 'You have successfully reported.'
            }
            return JsonResponse(data, safe=False)

    return redirect(reverse('channel', args=[str(slug)]))

def report_video(request, videoId):
    if not request.user.is_authenticated:
            current_url=request.get_full_path()
            login_url=reverse("account_login")
            login_required="{}?next={}".format(login_url, current_url)
            data={
                'login_required':login_required
            }
            return JsonResponse(data, safe=False)
    if request.method=="POST":
        video=VideoFiles.objects.get(id=videoId)
        report_reason=request.POST['report_reason']
        if not(len(report_reason)):
            data={
                'text_required': 'Please fill out this field.'
            }
            return JsonResponse(data, safe=False)
        else:
            ReportVideo.objects.get_or_create(video=video, reporter=request.user, report_reason=report_reason)
            data={
                'success_mes': 'You have successfully reported.'
            }
            return JsonResponse(data, safe=False)

    return redirect(reverse('video_watch', args=[str(videoId)]))

def remove_videos_playlist(request):
    if request.method=="POST":
        channel=Channel.objects.get(slug=request.user)
        videos=VideoFiles.objects.get(id=request.POST['video_id'])
        playlist=Playlist.objects.get(channel=channel)
        playlist.video.remove(videos)
        data={
            "videos_count": playlist.video.all().count(),
            "video_id": videos.id,
            "success_message": 'Removed !'
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('channel', args=[str(request.user)]))

def del_myvideos(request):
    if request.method=="POST":
        videos=VideoFiles.objects.get(id=request.POST['video_id'])
        videos.delete()
        data={
            "video_id": videos.id,
            "success_message": 'Deleted !'
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('channel', args=[str(request.user)]))

def edit_myvideos(request, video_id):
    channel = Channel.objects.get(user=request.user.id)
    last_login=User.objects.get(username=channel.slug).last_login
    videos_channel=VideoFiles.objects.filter(channel=channel)
    views_point=int(len(ViewCount.objects.filter(video__in=videos_channel))/int(10))
    if(views_point == int(0)):
        views_point=int(0)
    elif(views_point < int(1)):
        views_point=int(1)
    if request.method == "POST":
        channel=Channel.objects.get(slug=request.user)
        videos=VideoFiles.objects.get(id=video_id)
        other_category=Category.objects.all().exclude(name=videos.video_detail.category)
        context={
            'channel': channel,
            'mychannel': channel,
            'top_nav': channel,
            'last_login': last_login,
            'views_point': views_point,
            'categories': Category.objects.all(),
            'other_category': other_category,
            'videos': videos
        }
        return render(request, 'main/videos_edit.html', context)
    return redirect(reverse('channel', args=[str(request.user)]))

def processing_edit_myvideos(request, video_id):
    if request.method=="POST":
        videos=VideoFiles.objects.get(id=video_id)
        videos_detail=VideoDetail.objects.filter(videofile=videos)
        videos_detail.update(
            title=request.POST['title'], 
            description=request.POST['description'],
            category=request.POST['category'],
            visibility=request.POST['visibility']
            )
        if (request.FILES):
            videos_detail.update(thumbnail=request.FILES['thumbnail'])
        data={
            'success_mes':'Update successfully !!!'
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('channel', args=[str(request.user)]))