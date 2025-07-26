from rest_framework import serializers
from .models import Profile, Video

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'skills', 'languages', 'credibility_score']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user', 'title', 'description', 'file_url', 'created_at']
