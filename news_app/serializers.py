from django.contrib.auth.models import User
from rest_framework import serializers

from .models import News


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = News
        fields = ['id', 'title', 'summary', 'content', 'author', 'author_name', 'date_created']
        read_only_fields = ['author', 'author_name', 'date_created']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('Это поле обязательно.')
        return value

    def validate_content(self, value):
        if len(value.strip()) < 50:
            raise serializers.ValidationError('Минимум 50 символов.')
        return value

    def validate_summary(self, value):
        if value is not None and len(value) > 300:
            raise serializers.ValidationError('Максимум 300 символов.')
        return value
