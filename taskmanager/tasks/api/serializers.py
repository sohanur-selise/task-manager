from rest_framework import serializers
from tasks.models import Task, Comment
from users.models import User


class UserSerializerLight(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email'
        )


class CommentSerializer(serializers.ModelSerializer):
    commented_by = UserSerializerLight(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'commented_by',
            'task',

        ]


class CommentSerializerLight(serializers.ModelSerializer):
    commented_by = UserSerializerLight(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'commented_by'
        ]


class TaskSerializer(serializers.ModelSerializer):
    assigned_by = UserSerializerLight(read_only=True)
    assignee_details = UserSerializerLight(read_only=True, source='assignee')
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = Comment.objects.filter(task=obj)
        serializer = CommentSerializerLight(comments, many=True)
        return serializer.data

    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'description',
            'is_completed',
            'due_date',
            'assigned_by',
            'assignee',
            'assignee_details',
            'comments',
        )