from django.db import models
from users.models import User


class TemporalModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(TemporalModel):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_by', blank=True, null=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee', blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(TemporalModel):
    content = models.TextField()
    commented_by = models.ForeignKey(User, models.CASCADE, blank=True, null=True, related_name='commented_by_user')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name='task_comments')

    def __str__(self):
        return f"{self.content} -- {self.task.name}"