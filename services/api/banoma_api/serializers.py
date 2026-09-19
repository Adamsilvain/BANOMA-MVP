from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Video, Badge, Publication, Product, Purchase, Payment


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description']


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ['id', 'type', 'title', 'doi', 'year']


class ProfileSerializer(serializers.ModelSerializer):
    badges = BadgeSerializer(many=True, read_only=True)
    publications = PublicationSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'bio', 'skills', 'languages', 'credibility_score',
            'badges', 'google_scholar_url', 'publications',
        ]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user', 'title', 'description', 'file_url', 'created_at']
        read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'title', 'description', 'type', 'revenue_model',
            'price', 'currency', 'created_at', 'updated_at',
        ]
        read_only_fields = ['seller', 'created_at', 'updated_at']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'id', 'product', 'buyer', 'amount_paid', 'platform_commission',
            'creator_revenue', 'status', 'created_at',
        ]
        read_only_fields = ['buyer', 'platform_commission', 'creator_revenue', 'status', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'purchase', 'amount', 'currency', 'provider', 'status', 'reference', 'created_at']
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
