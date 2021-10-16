from django.db import models
from app.utils.constants import USER_ROLE


class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.TextField()
    email = models.CharField(max_length=64)
    role = models.CharField(max_length=16, default=USER_ROLE.USER, choices=USER_ROLE.choices())

    name = models.CharField(max_length=64, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=16, blank=True)
    dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'


NONE_USER = User(id='none_user', role=None)
