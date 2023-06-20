from django.urls import include, path
from rest_framework import routers
from users.api.views import UserViewSet, CustomObtainAuthToken

router = routers.DefaultRouter()
router.register(r"register", UserViewSet, basename="usercrud")

app_name = "users_api"

urlpatterns = [
    path("", include(router.urls)),
    path("login/", CustomObtainAuthToken.as_view(), name="token_auth"),
    path("list", UserViewSet.as_view({'get': 'list'}), name="user_list"),
    path("list/<int:pk>", UserViewSet.as_view({'get': 'retrieve'}), name="user_details"),
]
