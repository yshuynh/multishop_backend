# Generated by Django 3.2.8 on 2021-10-22 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_update_user_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='is_solved',
            field=models.BooleanField(default=True),
        ),
    ]