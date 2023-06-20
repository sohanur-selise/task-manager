from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('team_member', 'Team Member'),
    ]

    first_name = models.CharField(max_length=255, verbose_name="First name", null=True)
    last_name = models.CharField(max_length=255, verbose_name="Last name", null=True)
    email = models.EmailField(blank=True, verbose_name="Email address", null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='team_member')

    def __str__(self):
        return f"{self.email}"