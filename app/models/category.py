from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)
    thumbnail = models.CharField(max_length=64)
    brands = models.ManyToManyField('Brand', related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name
