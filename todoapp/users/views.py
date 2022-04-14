from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserCreateSerializer


class UserRegistrationAPIView(ModelViewSet):
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
    permission_classes = []
    http_method_names = ['post']
    serializer_class = UserCreateSerializer


class UserLoginAPIView():
    """
        success response format
         {
           auth_token: ""
         }
    """
