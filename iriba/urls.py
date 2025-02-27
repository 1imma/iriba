"""
URL configuration for iriba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from core.views import upload_video,home,content_feed,like_video,profile, add_comment, video_detail, notifications
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include  # Add include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page URL
    path('upload/', upload_video, name='upload_video'),  # Video upload URL
    path('accounts/', include('allauth.urls')),  # Add this line for Allauth
    path('feed/', content_feed, name='content_feed'),
    path('like/<int:video_id>/', like_video, name='like_video'),
    path('profile/<str:username>/', profile, name='profile'),
    path('comment/<int:video_id>/', add_comment, name='add_comment'),
    path('video/<int:video_id>/', video_detail, name='video_detail'),  # Add this line
    path('notifications/', notifications, name='notifications'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
