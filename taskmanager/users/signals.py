from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from users.models import User


@receiver(post_save, sender=User)
def create_user(sender, instance, **kwargs):
    if kwargs["created"]:
        Token.objects.create(user=instance)