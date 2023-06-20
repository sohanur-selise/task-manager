from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from users.api import responses
from users.models import User
from django.utils.text import slugify
from django.utils import timezone

from users.api.serializers import UserSerializer, UserAuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException, PermissionDenied
from django.contrib.auth.hashers import make_password


class CustomObtainAuthToken(ObtainAuthToken):
    user = None
    request = None

    def get_user_response(self) -> Response:
        token, created = Token.objects.get_or_create(user=self.user)
        data = UserSerializer(instance=self.user, context={"request": self.request}).data
        self.user.last_login = timezone.now()
        self.user.save()
        return responses.success(data)

    def post(self, request, *args, **kwargs):
        # Get username
        input = request.data.get("email", None)
        # password = request.data.get("password", None)
        user = User.objects.filter(email=input).first()
        if not user:
            raise PermissionDenied(
                responses.base_object(
                    success=False,
                    errors={"login": "Unable to log in with provided credentials"},
                )
            )

        data = {
            "username": user.username,
            "password": request.data.get("password", None),
        }
        serializer = UserAuthTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.request = request
        self.user = serializer.validated_data["user"]
        return self.get_user_response()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        permission_classes = (permissions.IsAuthenticated,)
        if self.action == "create":
            permission_classes = (permissions.AllowAny,)
        if self.action == "list":
            permission_classes = (permissions.AllowAny,)
        return [permission() for permission in permission_classes]

    def create(self, request):
        request_data = request.data

        date_string = slugify(timezone.now().strftime("%Y-%m-%d %H:%M:%S")).replace("-", "_")
        username = f"user_{date_string}"

        email = request.data.get('email', None)
        role = request.data.get('role', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        if "password" not in request_data:
            responses.error("Password can't be blank")
        if "role" not in request_data:
            responses.error("Role can't be blank")

        user = User.objects.filter(email=email).first()

        if user:
            return responses.error("Email/Phone already exists")

        hashed_password = make_password(request_data["password"])

        user = User.objects.create(
                username=username,
                password=hashed_password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=False,
                is_superuser=False,
                role=role,
            )
        user_auth = self.serializer_class(instance=user).data
        return responses.success(user_auth)

    def list(self, request, *args, **kwargs):
        users = self.queryset.all()
        # tasks = self.queryset.filter(created_by=request.user)
        serializer = self.serializer_class(users, many=True)
        return responses.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = self.queryset.filter(id=kwargs["pk"]).first()
        serializer = self.serializer_class(user, context={"request": request})
        return responses.success(serializer.data)