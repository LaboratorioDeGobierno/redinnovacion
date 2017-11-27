# rest framework
from rest_framework import serializers

# models
from platforms.models import Platform
from platforms.models import UserPlatformAttribute


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        exclude = ('token',)


class PlatformTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class UserPlatformAttributeSerializer(serializers.ModelSerializer):

    class DefaultPlatform(object):
        def set_context(self, field):
            self.auth = field.context['request'].auth

        def __call__(self, *args, **kwargs):
            return self.auth

    platform = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(),
        default=DefaultPlatform()
    )

    class Meta:
        model = UserPlatformAttribute
        fields = '__all__'
