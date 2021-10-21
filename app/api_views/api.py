from rest_framework import generics, status, exceptions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from app.exceptions import ClientException
from app.models import Category, Product, Brand
from app.models.user import User
from app.serializers import CategoryFullSerializer, ProductSerializer, CategorySerializer, BrandSerializer, \
    BrandFullSerializer, LoginSerializer, RegisterSerializer, ProductDetailSerializer
from app.utils import string_util


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            c_user = User.objects.get(username=username)
            # if not string_util.check_encrypted_string(password, c_user.password):
            if not c_user.check_password(password):
                raise ClientException('Incorrect password')
        except User.DoesNotExist:
            # raise exceptions.AuthenticationFailed('User not found.')
            raise ClientException('User not found.')
        serializer = self.get_serializer(c_user)
        response = Response(serializer.data)
        response.set_cookie('access_token', serializer.data.get('access_token'))
        return response


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListAPI(generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryFullSerializer

    def get(self, request, *arg, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class CategorySingleAPI(generics.GenericAPIView):
    queryset = Category.objects
    serializer_class = CategoryFullSerializer

    def get(self, request, pk, *arg, **kwargs):
        c_category = self.get_object()
        print(c_category.name)
        serializer = self.get_serializer(c_category)
        return Response(serializer.data)


class ProductListAPI(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *arg, **kwargs):
        category_id = request.query_params.get('category')
        queryset = self.get_queryset()
        if category_id is not None:
            queryset = self.get_queryset().filter(category=category_id)
        brand_id = request.query_params.get('brand')
        if brand_id is not None:
            queryset = self.get_queryset().filter(brand=brand_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class ProductSingleAPI(generics.GenericAPIView):
    queryset = Product.objects
    serializer_class = ProductDetailSerializer

    def get(self, request, pk, *arg, **kwargs):
        c_product = self.get_object()
        serializer = self.get_serializer(c_product)
        return Response(serializer.data)


class BrandListAPI(generics.GenericAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request, *arg, **kwargs):
        category_id = request.query_params.get('category')
        queryset = self.get_queryset()
        if category_id is not None:
            queryset = self.get_queryset().filter(categories=category_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BrandSingleAPI(generics.GenericAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request, pk, *arg, **kwargs):
        c_brand = self.get_object()
        serializer = self.get_serializer(c_brand)
        return Response(serializer.data)
