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
    User = apps.get_model('app', 'User')
    Product = apps.get_model('app', 'Product')
    Rating = apps.get_model('app', 'Rating')
    RatingResponse = apps.get_model('app', 'RatingResponse')

    ad_user = User.objects.create_superuser(
        username='ad',
        password='ad'
    )
    ad_user.name = "Huỳnh Tấn Ý"
    ad_user.role = USER_ROLE.ADMIN
    ad_user.save()
    user1 = User.objects.create_user(
        username='user1',
        password='123'
    )
    user1.name = "Lê Đức Lương"
    user1.save()

    c_product = Product.objects.all().first()
    c_rating = Rating.objects.create(
        rate=4,
        comment="Sao mình ms mua máy đc 2 ngày r , về chơi game pin lúc đầu là 90 chơi trận game khoảng 30 40p , thì nó lại tuột 40% pin , kh biết có bị lỗi pin kh",
        user=user1,
        product=c_product
    )
    c_rating.save()

    RatingResponse.objects.create(
        comment="Bạn hãy đến cửa hàng gần nhất để nhận khuyến mãi nhé.",
        user=ad_user,
        rating=c_rating
    ).save()

    RatingResponse.objects.create(
        comment="Cảm ơn admin.",
        user=user1,
        rating=c_rating
    ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_data'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
