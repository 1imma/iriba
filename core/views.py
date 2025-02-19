from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import ProfileForm, VideoForm, CommentForm
from .models import Profile, Video
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            print(f"User: {request.user}")  # Debug: Print the current user
            print(f"Video: {video.title}")  # Debug: Print the video title
            video.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})

def content_feed(request):
    videos = Video.objects.all().order_by('-created_at')  # Newest videos first
    print(videos)
    return render(request, 'content_feed.html', {'videos': videos})


def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.likes.all():
        video.likes.remove(request.user)  # Unlike the video
    else:
        video.likes.add(request.user)  # Like the video
    return redirect('content_feed')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    videos = Video.objects.filter(user=user).order_by('-created_at')
    return render(request, 'profile.html', {'profile_user': user, 'videos': videos})


def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
    return redirect('content_feed')