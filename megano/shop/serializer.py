from rest_framework import serializers
from django.contrib.auth.models import User

from shop.models import Comment, Product


class CommentSerializer(serializers.ModelSerializer):
    """ сериализатор для модели Comment"""

    class Meta:
        model = Comment
        fields = ['nickname', 'text', 'email']

    def validate(self, attrs):
        if not isinstance(self.context['request'].user, User):
            if 'email' not in attrs or 'nickname' not in attrs:
                raise serializers.ValidationError("email and nickname are required for unauthorized users")
            if attrs['email'] == '' or attrs['nickname'] == '':
                raise serializers.ValidationError("email and nickname cannot be empty for unauthorized")
        return attrs

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
