from django.shortcuts import render, redirect
from .forms import ProfileForm, VideoForm
from .models import Profile
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
            video.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})