from rest_framework import serializers, exceptions

from app.models import Category, Product, Brand
from app.models.rating import Rating, RatingResponse
from app.models.user import User
from app.utils import jwt_util, string_util


class LoginSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('access_token',)

    def get_access_token(self, obj):
        return jwt_util.extract_token(obj)


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


class RatingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingResponse
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }


class UserInfoLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class ProductRatingsSerializer(serializers.ModelSerializer):
    responses = serializers.SerializerMethodField()
    user = UserInfoLiteSerializer()

    class Meta:
        model = Rating
        exclude = ('product',)
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_responses(self, obj):
        return RatingResponseSerializer(obj.responses, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_avg_rating(self, obj):
        list_rate = obj.ratings.all().values_list('rate', flat=True)
        if len(list_rate) == 0:
            return 0
        return round(float(sum(list_rate)/len(list_rate)), 1)


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    ratings = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'thumbnail')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class CategoryFullSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    brands = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = tuple([field.name for field in model._meta.fields]) + ('products', 'brands')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_products(self, obj):
        data = obj.products.all().values_list('id', flat=True)
        return data

    def get_brands(self, obj):
        data = obj.brands.all().values_list('id', flat=True)
        return data

    # def to_representation(self, instance):
    #     data = super(CategoryFullSerializer, self).to_representation(instance)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        extra_kwargs = {
            'id': {'read_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'name', 'address', 'phone_number', 'dob')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = string_util.encrypt_string(validated_data['password'])
        instance = User.objects.create(**validated_data)
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
