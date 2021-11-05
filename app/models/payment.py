from django.db import models


class Payment(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=32)
    logo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment'
