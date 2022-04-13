from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.serializers import BaseUserSerializer
from todos.models import Todo

# Add your serializer(s) here


class BaseTodoSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    created_at = serializers.DateTimeField(source="date_created")
    creator = BaseUserSerializer(source='user')

    class Meta:
        model = Todo
        fields = ['id', 'name', 'status', 'created_at', 'creator']


class TodoSerializer(serializers.ModelSerializer):
    done = serializers.BooleanField()

    class Meta:
        model = Todo
        fields = ['name', 'done', 'date_created']


class UserTodoDateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(source="date_created")
    status = serializers.CharField()
    creator = serializers.SerializerMethodField()
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Todo
        fields = ['id', 'creator', 'email', 'name', 'status', 'created_at']

    def get_creator(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
