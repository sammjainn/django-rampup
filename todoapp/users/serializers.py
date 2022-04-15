from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

# Serializers for the User model


class UserIdSerializer(serializers.ModelSerializer):
    '''
    Serializer for User ID
    '''
    class Meta:
        model = User
        fields = ('id', )


class BaseUserSerializer(serializers.ModelSerializer):
    '''
    Serializer for User details
    '''
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserTodosBaseSerializer(BaseUserSerializer):
    '''
    Serializer for User Details and count of pending and completed todos
    '''
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + \
            ('pending_count', 'completed_count')


class UserDetailSerializer(UserIdSerializer, BaseUserSerializer):
    '''
    Serializer for User ID and User details
    '''
    class Meta:
        model = User
        fields = tuple(set(UserIdSerializer.Meta.fields +
                       BaseUserSerializer.Meta.fields))


class UserCompletedSerializer(UserDetailSerializer):
    '''
    Serializer for User ID and details and count of completed todos
    '''
    completed_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = UserDetailSerializer.Meta.fields + ('completed_count', )


class UserPendingSerializer(UserDetailSerializer):
    '''
    Serializer for User ID and details and count of pending todos
    '''
    pending_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = UserDetailSerializer.Meta.fields + ('pending_count', )


class UserTodosSerializer(UserCompletedSerializer, UserPendingSerializer):
    '''
    Serializer for User ID and details and count of completed todos
    '''
    class Meta:
        model = User
        fields = list(set(UserCompletedSerializer.Meta.fields +
                      UserPendingSerializer.Meta.fields))


class UserCreateSerializer(BaseUserSerializer):
    '''
    Serializer for User Registration
    '''
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + \
            ('password', 'date_joined', 'token')

    def get_token(self, obj):
        '''
        Generate token on registration
        '''
        return Token.objects.get(user=obj).key


class UserLoginSerializer(serializers.Serializer):
    '''
    Serializer for User Login
    '''
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        '''
        Validate credentials on login
        '''
        print(data['email'], data['password'])
        user = User.objects.filter(email=data['email'])
        if user is None:
            raise ValidationError('Incorrect email')
        return data
