# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    institution_name = serializers.ReadOnlyField(
        source='institution.name',
    )
    region_name = serializers.ReadOnlyField(
        source='region.name',
    )
    url_profile = serializers.URLField(
        source='get_absolute_url', read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'url_profile',
            'email',
            'charge',
            'institution',
            'institution_name',
            'region',
            'region_name',
            'avatar',
            'phone',
            'address',
            'get_full_name',
            'status',
            'get_status_display',
            'is_staff',
        )


class UserMentionSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer to meet user's schema of mention.js
    """
    username = serializers.ReadOnlyField(source='slug')
    image = serializers.ReadOnlyField(source='get_avatar_url')
    url = serializers.ReadOnlyField(source='get_absolute_url')

    class Meta:
        model = User
        fields = (
            'username',
            'image',
            'url',
            'id',
        )
