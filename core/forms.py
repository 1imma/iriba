from django import forms
from .models import Profile, Video,Comment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']