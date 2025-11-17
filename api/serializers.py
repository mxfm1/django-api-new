from django.contrib.auth.models import User
from rest_framework import serializers
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id","username","email","password"]
        extra_kwargs = {"password":{"write_only":True}}

    def create(self, validated_data):
        email = validated_data.get('email')
        print('user-created-email')
        if email in settings.ADMIN_EMAILS:
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)