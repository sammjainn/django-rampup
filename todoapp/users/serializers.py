from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model
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
        extra_kwargs = {'first_name': {'required': False},
                        'last_name': {'required': False}}

    def get_token(self, obj):
        '''
        Generate token on registration
        '''
        return Token.objects.get_or_create(user=obj)[0].key

    def validate(self, data):
        data['password'] = make_password(data['password'])
        return data


class UserLoginSerializer(serializers.Serializer):
    '''
    Serializer for User Login
    '''
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def validate(self, data):
        '''
        Validate credentials on login
        '''
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(email=email, password=password)

        if user is None:
            raise ValidationError('Incorrect credentials')

        return data

    def get_token(self, instance):
        user = User.objects.get(email=instance['email'])
        token, created = Token.objects.get_or_create(user=user)
        return token.key
