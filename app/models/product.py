from django.db import models


class Product(models.Model):
    name = models.TextField()
    description = models.TextField()
    thumbnail = models.TextField()
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='products')
    sale_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name
