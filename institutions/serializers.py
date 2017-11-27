# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Institution


class InstitutionSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = ('pk', 'name',)


class InstitutionSerializer(InstitutionSimpleSerializer):
    url_detail = serializers.URLField(
        source='get_absolute_url', read_only=True)

    class Meta(InstitutionSimpleSerializer.Meta):
        fields = (
            'pk',
            'name',
            'url_detail',
            'url',
            'address',
            'phone',
            'logo',
            'users_count',
        )
