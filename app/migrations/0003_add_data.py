from django.db import migrations
from rest_framework.utils import json

from server.settings import BASE_DIR


def create_data(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Product = apps.get_model('app', 'Product')
    Category = apps.get_model('app', 'Category')
    Brand = apps.get_model('app', 'Brand')
    with open(BASE_DIR / 'init_data.json', encoding='utf-8') as f:
        json_data = f.read()
    # print(json_data)
    json_data = json.loads(json_data)
    for category in json_data:
        m_category = Category.objects.create(
            name=category['categoryName'],
            thumbnail=category['categoryThumbnail']
        )
        m_category.save()
        for product in category['products']:
            try:
                m_brand = Brand.objects.get(name=product['brand'])
            except Brand.DoesNotExist:
                m_brand = Brand.objects.create(
                    name=product['brand']
                )
                m_brand.save()
            m_category.brands.add(m_brand)
            m_category.save()
            m_product = Product.objects.create(
                name=product['productName'],
                description=product['productDescription'],
                thumbnail=product['productThumbnail'],
                brand=m_brand,
                sale_price=product['salePrice'],
                category=m_category
            )
            m_product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_many_to_many_category_brand'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
