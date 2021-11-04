from django.db import models


class Image(models.Model):
    url = models.TextField()
    label = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'image'

