from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from todos.serializers import *
from todos.models import Todo
from todos.permissions import UserTodoPermissions


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
    lookup_url_kwarg = 'id'
    ordering = '-date_created'
    permission_classes = [UserTodoPermissions]

    def get_serializer_class(self):
        if self.action == 'create':
            return TodoCreateSerializer
        elif self.action == 'update':
            return TodoUpdateSerializer
        elif self.action == 'list' or self.action == 'retrieve':
            return UserTodoSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Todo.objects.filter(user=self.request.user)
        return Todo.objects.all()

    def get_object(self):
        if self.action == 'update':
            todo_id = self.request.data.get('todo_id')
            obj = get_object_or_404(Todo, id=todo_id)
        elif self.action == 'retrieve' or self.action == 'destroy':
            id = self.kwargs.get(self.lookup_url_kwarg)
            obj = get_object_or_404(Todo, id=id)
        self.check_object_permissions(self.request, obj)

        return obj
