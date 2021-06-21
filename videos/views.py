from os import name
from django.shortcuts import redirect, render
from .forms import EditChannelForm
from videos.models import Channel
from django.core.exceptions import ValidationError


# Create your views here.
def home_view(request):
    try:
        current_user = request.user
        user_id = current_user.id
        user_name = current_user.username
        try:
            myuser=Channel.objects.get(user=user_id)
        except:
            Channel.objects.get_or_create(name=user_name, user=current_user, slug=user_name)
            myuser=Channel.objects.get(user=user_id)
        context = {
            'myuser': myuser
        }
    except Exception as e:
        print(e)
        context = {
            'myuser': ''
        }
    return render(request, 'base.html', context)

def channel_view(request, slug):
    try:
        current_user = request.user
        user_id = current_user.id
        user_name = current_user.username
        myuser=Channel.objects.get(user=user_id)
        try:
            channel=Channel.objects.get(slug=slug)
            if user_name == slug:
                context = {
                    'channel': channel,
                    'myuser': myuser,
                    'my_channel': '1'
                }
            else:
                context = {
                    'channel': channel,
                    'myuser': myuser,
                }
            return render(request, 'channel.html', context)
        except:
            context = {
                'myuser': myuser
            }
            return redirect('index')
    except:
        return redirect('index')

def channel_edit_view(request, slug):
    try:
        current_user = request.user
        user_id = current_user.id
        user_name = current_user.username
        myuser=Channel.objects.get(user=user_id)
        mychannel=Channel.objects.get(slug=slug)
        if user_name == slug:
            if request.method =="POST":
                new_name=request.POST['name']
                if Channel.objects.filter(name=new_name).exists():
                    if mychannel.name == new_name:
                        form=EditChannelForm(request.POST, request.FILES, instance=mychannel)
                        if form.is_valid():
                            form.save()
                        return redirect('channel', slug=request.user)
                    else:
                        context={
                                'error_message': 'Channel "{0}" already exists !'.format(new_name),
                                'channel': mychannel,
                                'myuser': myuser
                                }
                else:
                    form=EditChannelForm(request.POST, request.FILES, instance=mychannel)
                    if form.is_valid():
                        form.save()
                    return redirect('channel', slug=request.user)
            else:
                form=EditChannelForm(instance=mychannel)
                context={
                    'edit_form': form,
                    'channel': mychannel,
                    'myuser': myuser

                }
            return render(request, 'channel_edit.html', context)
        else:
            return redirect('index')
    except:
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