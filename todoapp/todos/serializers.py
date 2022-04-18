from rest_framework import serializers
from users.serializers import BaseUserSerializer
from todos.models import Todo

# Serializers for the Todo model


class BaseTodoSerializer(serializers.ModelSerializer):
    '''
    Serializer for Todo details
    '''
    status = serializers.CharField()
    created_at = serializers.DateTimeField(source="date_created")
    creator = BaseUserSerializer(source='user')

    class Meta:
        model = Todo
        fields = ['id', 'name', 'status', 'created_at', 'creator']


class TodoSerializer(serializers.ModelSerializer):
    '''
    Serializer for Todo details and status
    '''
    class Meta:
        model = Todo
        fields = ('done',)


class TodoCreateSerializer(TodoSerializer):
    '''
    Serializer for creating a Todo
    '''
    user_id = serializers.IntegerField(write_only=True)
    name = serializers.CharField(read_only=True)
    todo = serializers.CharField(source='name', write_only=True)

    class Meta:
        model = Todo
        fields = TodoSerializer.Meta.fields + \
            ('name', 'date_created', 'user_id', 'todo')


class TodoUpdateSerializer(TodoSerializer):
    '''
    Serializer for updating a Todo
    '''
    todo_id = serializers.IntegerField(source='id')
    todo = serializers.CharField(source='name')

    class Meta:
        model = Todo
        fields = TodoSerializer.Meta.fields + ('todo_id', 'todo')

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.done = validated_data.get('done', instance.done)
        instance.save()
        return instance


class UserTodoSerializer(TodoUpdateSerializer):
    '''
    Serializer for Todo details and user ID
    '''
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Todo
        fields = TodoUpdateSerializer.Meta.fields + ('user_id', )


class UserTodoDateSerializer(serializers.ModelSerializer):
    '''
    Serializer for Todo and creator details
    '''
    created_at = serializers.DateTimeField(source="date_created")
    status = serializers.CharField()
    creator = serializers.SerializerMethodField()
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Todo
        fields = ['id', 'creator', 'email', 'name', 'status', 'created_at']

    def get_creator(self, obj):
        '''
        Creator name for Todo
        '''
        return obj.user.first_name + ' ' + obj.user.last_name
