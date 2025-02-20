from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
    

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)  # Add this line

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:50]}'
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User receiving the notification
    message = models.CharField(max_length=255)  # Notification message
    link = models.CharField(max_length=255, blank=True)  # Link to the related content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the notification
    is_read = models.BooleanField(default=False)  # Whether the notification has been read

    def __str__(self):
        return self.message
