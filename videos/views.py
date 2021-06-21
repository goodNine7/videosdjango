from os import name
from django.db import reset_queries
from django.shortcuts import redirect, render
from .forms import EditChannelForm
from videos.models import Channel
from django.core.exceptions import ValidationError


# Create your views here.
def home_view(request):
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
            'mychannel': channel
        }
    except:
        context = {
            'channel': '',
            'mychannel': ''
        }
    return render(request, 'base.html', context)


def channel_view(request, slug):
    try:
        channel = Channel.objects.get(slug=slug)
        if request.user.id:
            current_user = request.user
            mychannel = Channel.objects.get(user=current_user.id)
            context = {
                'channel': channel,
                'mychannel': mychannel
            }
        else:
            context = {
                'channel': channel,
                'mychannel': ''
            }
        return render(request, 'channel.html', context)
    except:
        return redirect('index')


def channel_edit_view(request, slug):
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
                        'mychannel': mychannel
                    }
                    # return render('channel', slug=request.user)
                else:
                    context = {
                        'error_message': 'Channel "{0}" already exists !'.format(new_name),
                        'channel': mychannel,
                        'mychannel': mychannel
                    }
            else:
                form = EditChannelForm(
                    request.POST, request.FILES, instance=mychannel)
                if form.is_valid():
                    form.save()
                context = {
                    'success_message': 'The information was updated successfully.',
                    'channel': mychannel,
                    'mychannel': mychannel
                }
                # return redirect('channel', slug=request.user)
        else:
            form = EditChannelForm(instance=mychannel)
            context = {
                'edit_form': form,
                'channel': mychannel,
                'mychannel': mychannel
            }
        return render(request, 'channel_edit.html', context)
    else:
        return redirect('index')


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
