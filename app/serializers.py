from rest_framework import serializers

from app.models import Category, Product, Brand


class BrandFullSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = '__all__'
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


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'thumbnail')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class CategoryFullSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_products(self, obj):
        data = obj.products.all().values_list('id', flat=True)
        return data

    # def to_representation(self, instance):
    #     data = super(CategoryFullSerializer, self).to_representation(instance)
