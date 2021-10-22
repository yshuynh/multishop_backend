from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'brand'

    def __str__(self):
        return self.name
