from rest_framework import serializers

from app.models import Category, Product, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('brands',)


class CategoryFullSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_products(self, obj):
        serializer = ProductSerializer(obj.products.all(), many=True)
        return serializer.data

    # def to_representation(self, instance):
    #     data = super(CategoryFullSerializer, self).to_representation(instance)
