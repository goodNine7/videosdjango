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


def channel_view(request, slug):
    mychannel=Channel.objects.get(slug=slug)
    context = {
        'channel': mychannel
    }
    return render(request, 'channel.html', context)

def channel_edit_view(request, slug):
    mychannel=Channel.objects.get(slug=slug)
    if request.method =="POST":
        new_name=request.POST['name']
        # list_name=[]
        # all_name=Channel.objects.all()
        # for x in all_name:
        #     list_name.append(str(x))
        # if new_name not in list_name:
        if not Channel.objects.filter(name=new_name).exists():
            form=EditChannelForm(request.POST, request.FILES, instance=mychannel)
            if form.is_valid():
                form.save()
            return redirect('channel', slug=request.user)
        else:
            raise ValidationError("You have forgotten about Fred!")

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