from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

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
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.action == 'create':
            return TodoCreateSerializer
        elif self.action == 'update':
            return TodoUpdateSerializer
        elif self.action == 'list' or self.action == 'retrieve':
            return UserTodoSerializer

    def get_queryset(self):
        if self.action == 'list' or self.action == 'create':
            user_id = self.request.data.get('user_id')
            return Todo.objects.filter(user=user_id)
        return Todo.objects.all()

    def get_object(self):
        if self.action == 'update':
            todo_id = self.request.data.get('todo_id')
            return get_object_or_404(Todo, id=todo_id)
        elif self.action == 'retrieve' or self.action == 'destroy':
            id = self.kwargs.get(self.lookup_url_kwarg)
            return get_object_or_404(Todo, id=id)
