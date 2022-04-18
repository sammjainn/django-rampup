from django.urls import path
from projects.views import ProjectMemberApiViewSet

app_name = 'projects'

urlpatterns = [
    path('<int:id>/add-users',
         ProjectMemberApiViewSet.as_view({'post': 'create'})),
    # path('<int:id>/remove-users', ProjectMemberApiViewSet.as_view(
    #     {'patch': 'update'})),
]
