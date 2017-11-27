# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import County, Region


class CountySerializer(serializers.ModelSerializer):

    class Meta:
        model = County
        fields = (
            'pk',
            'name',
            'region',
        )


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = (
            'pk',
            'name',
            'short_name',
        )
