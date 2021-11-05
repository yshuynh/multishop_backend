from django.db import models


class Cart(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='carts')
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'
