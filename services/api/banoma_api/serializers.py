from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Video, Opportunity, Application, Payment


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'skills', 'languages', 'credibility_score']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user', 'title', 'description', 'file_url', 'created_at']
        read_only_fields = ['created_at']


class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ['id', 'posted_by', 'title', 'description', 'type', 'location', 'remote', 'created_at']
        read_only_fields = ['created_at']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'opportunity', 'applicant', 'message', 'status', 'created_at']
        read_only_fields = ['applicant', 'status', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'currency', 'provider', 'status', 'reference', 'created_at']
        read_only_fields = ['user', 'status', 'reference', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'full_name']

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, bio='', skills='', languages='')
        first, _, last = full_name.partition(' ')
        user.first_name, user.last_name = first, last
        user.save()
        return user
