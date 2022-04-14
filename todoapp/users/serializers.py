from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

# Add your serializers


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserTodosBaseSerializer(BaseUserSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + \
            ('pending_count', 'completed_count')


class UserDetailSerializer(UserIdSerializer, BaseUserSerializer):
    class Meta:
        model = User
        fields = tuple(set(UserIdSerializer.Meta.fields +
                       BaseUserSerializer.Meta.fields))


class UserCompletedSerializer(UserDetailSerializer):
    completed_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = UserDetailSerializer.Meta.fields + ('completed_count', )


class UserPendingSerializer(UserDetailSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = UserDetailSerializer.Meta.fields + ('pending_count', )


class UserTodosSerializer(UserCompletedSerializer, UserPendingSerializer):
    class Meta:
        model = User
        fields = list(set(UserCompletedSerializer.Meta.fields +
                      UserPendingSerializer.Meta.fields))


class UserCreateSerializer(BaseUserSerializer):
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + \
            ('password', 'date_joined', 'token')

    def get_token(self, obj):
        return Token.objects.get(user=obj).key
