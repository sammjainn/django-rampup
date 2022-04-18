from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import UserCreateSerializer, UserLoginSerializer

User = get_user_model()


class UserRegistrationAPIView(CreateAPIView):
    '''
    View for registering user
    '''
    """
        success response format
         {
           first_name: "",
           last_name: "",
           email: "",
           date_joined: "",
           "token"
         }
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class UserLoginAPIView(CreateAPIView):
    '''
    View for performing user login
    '''
    """
        success response format
         {
           auth_token: ""
         }
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
