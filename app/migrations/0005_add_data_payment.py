from django.db import migrations
from rest_framework.utils import json

from app.utils.constants import USER_ROLE
from server.settings import BASE_DIR


def get_category_thumbnail(category_name):
    data = {
        'Laptop': 'fas fa-laptop',
        "Bàn phím": "fas fa-keyboard",
        "Chuột": "fas fa-mouse",
        "Tai nghe": "fas fa-headphones",
        "Tay cầm chơi game": "fab fa-xbox",
        "PC": "fas fa-hdd",
        "Màn hình": "fas fa-desktop",
        "Ghế Gaming": "fas fa-chair",
    }
    return data[category_name]


def create_data(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Payment = apps.get_model('app', 'Payment')
    Payment.objects.create(
        name='Thanh toán trực tiếp',
        code='cash',
        logo='https://thumbs.dreamstime.com/b/cash-logo-icon-design-vector-illustration-template-210732344.jpg'
    ).save()
    Payment.objects.create(
        name='Thanh toán bằng ví điện tử Momo',
        code='momo',
        logo='https://i2.wp.com/cdn.getapk.app/imgs/f/0/0/f00de8182a8a5d0dee60dc9f4d7c8d36_icon.jpg'
    ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_add_cart_order_payment'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
