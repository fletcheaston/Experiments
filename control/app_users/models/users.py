from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.functions import Lower
from simple_history.models import HistoricalRecords

from utils.models import DjangoModel


class UserQuerySet(models.QuerySet["User"]):
    pass


class UserManager(BaseUserManager["User"]):
    def create_user(
        self,
        name: str,
        email: str,
        **extra_fields: Any,
    ) -> "User":
        if not name:
            raise ValueError("Name must be provided.")

        if not email:
            raise ValueError("Email must be provided.")

        # Create the user in our system
        user: User = self.model(
            name=name,
            email=email,
            **extra_fields,
        )

        user.save()

        return user

    def create_superuser(
        self,
        name: str,
        email: str,
        **extra_fields: Any,
    ) -> "User":
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True

        return self.create_user(name, email, **extra_fields)


class User(DjangoModel, AbstractBaseUser, PermissionsMixin):
    ############################################################################
    # Normal fields
    name = models.TextField(default="")
    email = models.TextField(unique=True)

    suspended = models.BooleanField(default=False)

    # Django user fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    ############################################################################
    # Queryset managers
    objects = UserManager.from_queryset(UserQuerySet)()

    history = HistoricalRecords()

    ############################################################################
    # Meta
    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("email"), name="unique_email"),
        ]

    ############################################################################
    # Properties

    ############################################################################
    # Methods
