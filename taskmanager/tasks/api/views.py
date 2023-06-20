from rest_framework import permissions, viewsets, generics
from rest_framework.authentication import TokenAuthentication
from users.api import responses
from tasks.api.permission import CanCreateTaskPermission
from tasks.models import Task, Comment
from tasks.api.serializers import TaskSerializer, CommentSerializer
import django_filters
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
import datetime
from tasks.api.paginate import StandardResultsSetPagination


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset
        is_completed = self.request.query_params.get("is_completed", None)
        name = self.request.query_params.get("name", None)
        assignee = self.request.query_params.get("assignee", None)
        due_date = self.request.query_params.get("due_date", None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if assignee is not None:
            queryset = queryset.filter(assignee=assignee)
        if due_date is not None:
            try:
                queryset = queryset.filter(due_date__lte=due_date)
            except Exception:
                print('error in format')
                queryset = queryset

        if is_completed is not None:
            is_completed = is_completed.lower() == 'true'
            queryset = queryset.filter(is_completed=is_completed)
        return queryset

    def get_permissions(self):
        permission_classes = (permissions.IsAuthenticated,)
        if self.action == "create":
            permission_classes = (permissions.IsAuthenticated,)
        if self.action == "list":
            permission_classes = (permissions.IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if self.request.user.role != 'admin':
            queryset = queryset.filter(Q(assigned_by=self.request.user) | Q(assignee=self.request.user))
        serializer = self.serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            pagination = True
            serializer = self.serializer_class(
                page, context={"request": request}, many=True
            )
            response = self.get_paginated_response(serializer.data)
            return responses.success(response.data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            task = serializer.save(assigned_by=request.user)
            return responses.success(serializer.data)
        return responses.error(serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        task = self.queryset.filter(id=kwargs["pk"]).first()
        if task:
            serializer = self.serializer_class(task, context={"request": request})
            return responses.success(serializer.data)
        return responses.error('no task found')

    def update(self, request, *args, **kwargs):
        task = self.queryset.filter(id=kwargs["pk"]).first()
        if task:
            serializer = self.serializer_class(task, data=request.data, partial=True)
            if serializer.is_valid():
                updated_task = serializer.save()
                return responses.success(serializer.data)
            return responses.success(serializer.errors)
        return responses.error('task not found')

    def delete(self, request, *args, **kwargs):
        task = self.queryset.filter(id=kwargs["pk"]).first()
        if task:
            task.delete()
            return responses.success('deleted successfully')
        return responses.error('task not found')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        permission_classes = (permissions.IsAuthenticated,)
        if self.action == "create":
            permission_classes = (permissions.IsAuthenticated,)
        if self.action == "list":
            permission_classes = (permissions.IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, commented_by=request.user)
            return responses.success(serializer.data)
        return responses.error(serializer.errors)

    def list(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        comments = self.queryset.filter(task_id=task_id)
        serializer = self.get_serializer(comments, many=True)
        page = self.paginate_queryset(comments)
        if page is not None:
            pagination = True
            serializer = self.serializer_class(
                page, context={"request": request}, many=True
            )
            response = self.get_paginated_response(serializer.data)
            return responses.success(response.data)
        return responses.success(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return responses.success(serializer.data)
        return responses.error(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.success('deleted')

