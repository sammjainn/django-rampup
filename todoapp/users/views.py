from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView

from users.serializers import UserCreateSerializer


class UserRegistrationAPIView(CreateAPIView):
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
    serializer_class = UserCreateSerializer


class UserLoginAPIView():
    """
        success response format
         {
           auth_token: ""
         }
    """
