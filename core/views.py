from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import ProfileForm, VideoForm, CommentForm
from .models import Profile, Video,Notification
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
    videos_list = Video.objects.all().order_by('-created_at')  # Fetch all videos, newest first
    paginator = Paginator(videos_list, 5)  # Show 5 videos per page
    page_number = request.GET.get('page')  # Get the current page number from the URL
    videos = paginator.get_page(page_number)  # Get the videos for the current page
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


@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)  # Get the video being commented on
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Don't save to the database yet
            comment.user = request.user  # Assign the current user to the comment
            comment.video = video  # Assign the video to the comment
            comment.save()  # Save the comment to the database
            if request.user != video.user:  # Don't notify if the user comments on their own video
                Notification.objects.create(
                    user=video.user,
                    message=f'{request.user.username} commented on your video: {video.title}',
                    link=f'/video/{video.id}/'
                )
    return redirect('content_feed')  # Redirect back to the content feed


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)  # Get the video by ID
    return render(request, 'video_detail.html', {'video': video})


def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.likes.all():
        video.likes.remove(request.user)  # Unlike the video
    else:
        video.likes.add(request.user)  # Like the video
        # Create a notification for the video owner
        if request.user != video.user:  # Don't notify if the user likes their own video
            Notification.objects.create(
                user=video.user,
                message=f'{request.user.username} liked your video: {video.title}',
                link=f'/video/{video.id}/'
            )
    return redirect('content_feed')

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})