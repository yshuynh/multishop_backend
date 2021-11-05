import jwt
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, exceptions

from app.models import Category, Product, Brand, Image
from app.models.rating import Rating, RatingResponse
from app.models.user import User
from app.utils import jwt_util, string_util
from app.utils.constants import TOKEN_TYPE, ERROR_MESSAGE


class LoginSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('refresh_token', 'access_token', 'username', 'password')
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True}
        }

    def get_access_token(self, obj):
        return jwt_util.extract_token(obj, TOKEN_TYPE.ACCESS)

    def get_refresh_token(self, obj):
        return jwt_util.extract_token(obj, TOKEN_TYPE.REFRESH)


class RefreshTokenSerializer(serializers.Serializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.CharField(write_only=True)

    def __init__(self, instance=None, data=None, **kwargs):
        super(RefreshTokenSerializer, self).__init__(instance, data, **kwargs)
        self.user = None

    def validate_refresh_token(self, jwt_value):
        try:
            payload = jwt_util.extract_payload(jwt_value)
        except jwt.ExpiredSignatureError:
            msg = ERROR_MESSAGE.TOKEN_EXPIRED
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError as e:
            msg = ERROR_MESSAGE.TOKEN_DECODING_ERROR
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()
        if payload.get('type') != TOKEN_TYPE.REFRESH:
            raise exceptions.AuthenticationFailed(ERROR_MESSAGE.TOKEN_WRONG_TYPE_REFRESH)
        self.user = User.objects.get(id=payload.get('id'))

    def get_access_token(self, obj):
        return jwt_util.extract_token(self.user, TOKEN_TYPE.ACCESS)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'label', 'url')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class SpecificationsSerializer(serializers.CharField):
    specifications = serializers.CharField()

    def to_internal_value(self, data):
        print(data)
        return data

    def to_representation(self, value):
        data = super(SpecificationsSerializer, self).to_representation(value)
        list_data = value.split('\n')
        res = []
        for e in list_data:
            item_list = e.split(':')
            res.append({
                'name': item_list[0],
                'value': item_list[1] if len(item_list) > 1 else '',
            })
        return res


class BrandFullSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = tuple([field.name for field in model._meta.fields]) + ('products', 'categories')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_products(self, obj):
        data = obj.products.all().values_list('id', flat=True)
        return data

    def get_categories(self, obj):
        data = obj.categories.all().values_list('id', flat=True)
        return data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class UserInfoLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'role')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class RatingResponseLiteSerializer(serializers.ModelSerializer):
    user = UserInfoLiteSerializer()

    class Meta:
        model = RatingResponse
        exclude = ('rating', 'id')


class ProductRatingsSerializer(serializers.ModelSerializer):
    responses = serializers.SerializerMethodField()
    user = UserInfoLiteSerializer()

    class Meta:
        model = Rating
        fields = tuple([field.name for field in model._meta.fields]) + ('responses',)
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_responses(self, obj):
        return RatingResponseLiteSerializer(obj.responses, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'thumbnail')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    avg_rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'thumbnail', 'brand', 'price', 'sale_price', 'discount', 'created_at', 'updated_at', 'category', 'short_description', 'avg_rating')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_avg_rating(self, obj):
        list_rate = obj.ratings.all().values_list('rate', flat=True)
        if len(list_rate) == 0:
            return 0
        return round(float(sum(list_rate)/len(list_rate)), 1)

    def get_discount(self, obj):
        return int(float((obj.price-obj.sale_price) / obj.price)*100)


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    ratings = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    images = serializers.SerializerMethodField()
    specifications = SpecificationsSerializer()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = tuple([field.name for field in model._meta.fields if field.name not in ['price', 'sale_price']]) + ('price', 'sale_price', 'discount', 'avg_rating', 'brand', 'ratings', 'images')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_ratings(self, obj):
        serializer = ProductRatingsSerializer(obj.ratings, many=True)
        return serializer.data

    def get_avg_rating(self, obj):
        list_rate = obj.ratings.all().values_list('rate', flat=True)
        if len(list_rate) == 0:
            return 0
        return round(float(sum(list_rate)/len(list_rate)), 1)

    def get_images(self, obj):
        serializer = ImageSerializer(obj.images.all(), many=True)
        return serializer.data

    def get_discount(self, obj):
        return int(float((obj.price-obj.sale_price) / obj.price)*100)


class CategoryFullSerializer(serializers.ModelSerializer):
    # products = serializers.SerializerMethodField()
    brands = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = tuple([field.name for field in model._meta.fields]) + ('brands',)
        extra_kwargs = {
            'id': {'read_only': True}
        }

    # def get_products(self, obj):
    #     data = obj.products.all().values_list('id', flat=True)
    #     return data

    def get_brands(self, obj):
        serializer = BrandSerializer(obj.brands.all(), many=True)
        return serializer.data

    # def to_representation(self, instance):
    #     data = super(CategoryFullSerializer, self).to_representation(instance)


class UserSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%Y-%m-%d'], required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'name', 'address', 'phone_number',
                   'dob', 'created_at', 'updated_at')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
            'email': {'required': False},
            'role': {'read_only': True},
            'name': {'required': False},
            'address': {'required': False},
            'phone_number': {'required': False},
            'dob': {'required': False},
        }


class RegisterSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%Y-%m-%d'], required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'name', 'address', 'phone_number', 'dob', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'email': {'required': False},
            'dob': {'required': False}
        }

    def create(self, validated_data):
        # validated_data['password'] = string_util.encrypt_string(validated_data['password'])
        instance = User.objects.create_user(**validated_data)
        instance.password = make_password(validated_data['password'])
        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'address', 'phone_number', 'dob')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class UserRateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def to_representation(self, instance):
        data = super(UserRateProductSerializer, self).to_representation(instance)
        data['user'] = UserInfoLiteSerializer(User.objects.get(id=data['user'])).data
        return data


class RatingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingResponse
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def to_representation(self, instance):
        data = super(RatingResponseSerializer, self).to_representation(instance)
        data['user'] = UserInfoLiteSerializer(User.objects.get(id=data['user'])).data
        return data
