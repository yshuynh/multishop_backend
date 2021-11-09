from django.db import models

from app.utils.constants import ORDER_STATUS


class Order(models.Model):
    status = models.CharField(max_length=32, default=ORDER_STATUS.WAITING_CONFIRM, choices=ORDER_STATUS.choices())
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orders')
    is_paid = models.BooleanField(default=False)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=64)
    address = models.TextField()
    phone_number = models.CharField(max_length=16)
    sum_price = models.IntegerField(default=0)
    shipping_fee = models.IntegerField(default=0)
    total_cost = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'


class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items')
    count = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    order_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_item'
