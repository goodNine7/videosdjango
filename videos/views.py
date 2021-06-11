from django.shortcuts import render

# Create your views here.
def home_view(request):
    state = {
        'context': 'Home_View'
    }
    return render(request, 'base.html', state)

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

def user_view(request):
    state = {
        'context': ''
    }
    return render(request, 'user.html', state)

def upload_video_view(request):
    state = {
        'context': ''
    }
    return render(request, 'upload_videos.html', state)

def user_edit_view(request):
    state = {
        'context': ''
    }
    return render(request, 'user_edit.html', state)

def user_avatar_view(request):
    state = {
        'context': ''
    }
    return render(request, 'user_avatar.html', state)