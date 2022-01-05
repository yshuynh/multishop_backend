from django.db import models

from app.utils import email_util
from app.utils.constants import ORDER_STATUS


class Order(models.Model):
    status = models.CharField(max_length=32, default=ORDER_STATUS.WAITING_CONFIRM, choices=ORDER_STATUS.choices())
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orders', null=True)
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

    def save(self, *args, **kwargs):
        print('saving...')
        if self.status != ORDER_STATUS.WAITING_CONFIRM:
            data = {
                'id': self.id,
                'status': self.status,
                'name': self.name,
                'phone_number': self.phone_number,
                'address': self.address,
                'total_cost': self.total_cost,
                'items': [],
                'email': self.user.email
            }
            for item in self.items.all():
                data['items'].append({
                    'product':  {'name':item.product.name},
                    'count': item.count
                })
            email_util.send_order_email(data)
        super(Order, self).save(**kwargs)


class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items')
    count = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    order_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_item'
