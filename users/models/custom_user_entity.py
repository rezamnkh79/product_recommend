from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUserEntity(AbstractUser):
    location = models.CharField(max_length=255, null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)

    # Set related_name to avoid clash
    groups = models.ManyToManyField(
        Group,
        related_name='customuserentity_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuserentity_set',
        blank=True,
    )
