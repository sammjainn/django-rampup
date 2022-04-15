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
    class Meta:
        model = Todo
        fields = ('done',)


class TodoCreateSerializer(TodoSerializer):
    user_id = serializers.IntegerField(write_only=True)
    name = serializers.CharField(read_only=True)
    todo = serializers.CharField(source='name', write_only=True)

    class Meta:
        model = Todo
        fields = TodoSerializer.Meta.fields + \
            ('name', 'date_created', 'user_id', 'todo')


class TodoUpdateSerializer(TodoSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo = serializers.CharField(source='name')

    class Meta:
        model = Todo
        fields = TodoSerializer.Meta.fields + ('todo_id', 'todo')
        
    def create(self, validated_data):
        instance = Todo.objects.get(id=validated_data['id'])
        instance.id = validated_data['id']
        instance.name = validated_data['name']
        instance.done = validated_data['done']
        instance.save()
        return instance


class UserTodoSerializer(TodoUpdateSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Todo
        fields = TodoUpdateSerializer.Meta.fields + ('user_id', )


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
