from django.urls import path
from todos.views import TodoAPIViewSet

app_name = 'todos'

urlpatterns = [
    path('<int:id>/',
         TodoAPIViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('', TodoAPIViewSet.as_view(
        {'get': 'list', 'post': 'create', 'patch': 'create'}), name="register"),
]
