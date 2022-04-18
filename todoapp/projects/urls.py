from django.urls import path

from projects.views import ProjectMemberApiViewSet

app_name = 'projects'

urlpatterns = [
    path('<int:id>/<str:type>',
         ProjectMemberApiViewSet.as_view({'patch': 'update'}))
]
