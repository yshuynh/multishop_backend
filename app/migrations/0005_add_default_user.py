from django.db import migrations
from rest_framework.utils import json

from app.utils import string_util
from app.utils.constants import USER_ROLE
from server.settings import BASE_DIR


def create_data(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model('app', 'User')
    User.objects.create(
        username='admin',
        password=string_util.encrypt_string('123'),
        email='admin@admin.com',
        role=USER_ROLE.ADMIN,
    ).save()
    User.objects.create(
        username='user1',
        password=string_util.encrypt_string('123'),
        email='user1@user.com',
        role=USER_ROLE.USER,
    ).save()


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0004_create_user_model'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
