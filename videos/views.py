from typing import Text
from django.shortcuts import redirect, render
from .forms import EditChannelForm
from videos.models import Channel

# Create your views here.
def home_view(request):
    try:
        current_user = request.user
        user_id = current_user.id
        user_name = current_user.username
        try:
            mychannel=Channel.objects.get(user=user_id)
        except:
            Channel.objects.get_or_create(name=user_name, user=current_user, slug=user_name)
            mychannel=Channel.objects.get(user=user_id)
        context = {
            'channel': mychannel
        }
    except Exception as e:
        print(e)
        context = {
            'channel': ''
        }
    return render(request, 'base.html', context)

def login_view(request):
    state = {
        'context': ''
    }
    return render(request, 'login.html', state)

def sign_up_view(request):
    state = {
        'context': ''
    }
    return render(request, 'sign_up.html', state)

def logout_view(request):
    state = {
        'context': ''
    }
    return render(request, 'logout.html', state)

def channel_view(request, slug):
    mychannel=Channel.objects.get(slug=slug)
    context = {
        'channel': mychannel
    }
    return render(request, 'channel.html', context)

def channel_edit_view(request, slug):
    mychannel=Channel.objects.get(slug=slug)
    if request.method =="POST":
        form=EditChannelForm(request.POST, request.FILES, instance=mychannel)
        if form.is_valid():
            form.save()
            return redirect('channel', slug=request.user)
    else:
        form=EditChannelForm(instance=mychannel)
        context={
            'edit_form': form,
            'channel': mychannel
        }
    return render(request, 'channel_edit.html', context)

def upload_video_view(request):
    state = {
        'context': ''
    }
    return render(request, 'upload_videos.html', state)

def user_avatar_view(request):
    state = {
        'context': ''
    }
    return render(request, 'user_avatar.html', state)