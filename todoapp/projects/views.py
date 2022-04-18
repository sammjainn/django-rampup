from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projects.models import Project
from projects.serializers import AddMemberSerializer, RemoveMemberSerializer


class ProjectMemberApiViewSet(ModelViewSet):
    """
       constraints
        - a user can be a member of max 2 projects only
        - a project can have at max N members defined in database for each project
       functionalities
       - add users to projects

         Request
         { user_ids: [1,2,...n] }
         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }
         following are the possible status messages
         case1: if user is added successfully then - "Member added Successfully"
         case2: if user is already a member then - "User is already a Member"
         case3: if user is already added to 2 projects - "Cannot add as User is a member in two projects"

         there will be many other cases think of that

       - update to remove users from projects

         Request
         { user_ids: [1,2,...n] }

         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }

         there will be many other cases think of that and share on forum
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'id'
    serializer_class = AddMemberSerializer

    def get_object(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        object = Project.objects.filter(id=id).annotate(count=Count('members'))

        if object.exists():
            return object.first()
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_serializer_class(self):
        type = self.kwargs.get('type')
        if type == 'add-users':
            return AddMemberSerializer
        elif type == 'remove-users':
            return RemoveMemberSerializer
