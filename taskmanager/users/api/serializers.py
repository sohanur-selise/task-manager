# from django.contrib.auth import authentication

from rest_framework import serializers

from users.models import User

from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ParseError, PermissionDenied
from users.api import responses
from tasks.api.serializers import TaskSerializer


class UserAuthTokenSerializer(AuthTokenSerializer):
    """
    We extend this so we can create our own error messages

    We *only* use this when logging in Users/Customers
    """

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                raise PermissionDenied(
                    responses.base_object(
                        success=False,
                        errors={"login": "Unable to log in with provided credentials"},
                    )
                )
        else:
            raise ParseError(
                responses.base_object(
                    success=False,
                    errors={"login": 'Must include "email" and "password'},
                )
            )
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True, source="auth_token.key")
    tasks = TaskSerializer(many=True, read_only=True, source="assignee")

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "token",
            "role",
            "tasks",
        )
