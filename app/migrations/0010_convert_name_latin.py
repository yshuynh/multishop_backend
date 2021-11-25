from django.db import migrations
from rest_framework.utils import json

from app.utils.string_util import convert_vietnamese_to_latin
from server.settings import BASE_DIR

def create_data(apps, schema_editor):
    Product = apps.get_model('app', 'Product')
    product_list = Product.objects.all()
    for e in product_list:
        e.name_latin = convert_vietnamese_to_latin(e.name)
        e.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_add_field_name_latin'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
