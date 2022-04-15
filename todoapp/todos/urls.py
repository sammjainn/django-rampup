from rest_framework import routers
from django.urls import path
from todos.views import TodoAPIViewSet

app_name = 'todos'


router = routers.DefaultRouter()


urlpatterns = [
    path('<int:id>/',
         TodoAPIViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('', TodoAPIViewSet.as_view(
        {'get': 'list', 'post': 'create', 'patch': 'create'}), name="register"),
]
