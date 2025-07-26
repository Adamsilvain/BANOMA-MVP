from django.urls import path
from .views import VideoUploadView, ProfileView

urlpatterns = [
    path('videos/', VideoUploadView.as_view(), name='video-upload'),
    path('profiles/<int:user_id>/', ProfileView.as_view(), name='profile'),
]
