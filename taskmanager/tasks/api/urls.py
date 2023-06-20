
from django.urls import include, path
from rest_framework import routers
from tasks.api.views import TaskViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r'tasks/(?P<task_id>\d+)/comments', CommentViewSet, basename='task-comments')

app_name = "tasks_api"

urlpatterns = [
    path("", include(router.urls)),
    path("list/", TaskViewSet.as_view({'get': 'list'}), name="task_list"),
    path("create/", TaskViewSet.as_view({'post': 'create'}), name="task_create"),
    path("list/<int:pk>/", TaskViewSet.as_view({'get': 'retrieve'}), name="task_retrieve"),
    path("<int:pk>/", TaskViewSet.as_view({'put': 'update'}), name="task_update"),
    path("<int:pk>/", TaskViewSet.as_view({'destroy': 'delete'}), name="task_delete"),
]