from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from app.utils.constants import USER_ROLE


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, unique=True)
    password = models.TextField()
    email = models.CharField(max_length=64)
    role = models.CharField(max_length=16, default=USER_ROLE.USER, choices=USER_ROLE.choices())

    name = models.CharField(max_length=64, blank=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = 'user'


NONE_USER = User(id=9999999999, role=None)
