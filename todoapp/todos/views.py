from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from todos.serializers import *

from todos.models import Todo


class TodoAPIViewSet(ModelViewSet):
    '''
    View for editing, viewing, deleting Todos
    '''
    """
        success response for create/update/get
        {
          "name": "",
          "done": true/false,
          "date_created": ""
        }

        success response for list
        [
          {
            "name": "",
            "done": true/false,
            "date_created": ""
          }
        ]
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return TodoCreateSerializer
        elif self.action == 'update' or self.action == 'retrieve':
            return TodoUpdateSerializer
        elif self.action == 'list':
            return UserTodoSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Todo.objects.filter(user=self.request.data.get('user_id'))
        else:
            return Todo.objects.all()
