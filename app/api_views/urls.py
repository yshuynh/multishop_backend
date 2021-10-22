from django.urls import path, include
from .api import *

urlpatterns = [
    path('categories', CategoryListAPI.as_view(), name='category_list'),
    path('categories/<str:pk>', CategorySingleAPI.as_view(), name='category_single'),
    path('products', ProductListAPI.as_view(), name='product_list'),
    path('products/<str:pk>', ProductSingleAPI.as_view(), name='product_single'),
    path('brands', BrandListAPI.as_view(), name='brand_list'),
    path('brands/<str:pk>', BrandSingleAPI.as_view(), name='brand_single'),
    path('ratings/<str:pk>', RatingListProductAPI.as_view(), name='ratings_of_product'),
    # path('single/<str:pk>', CategoryDetailAPI.as_view(), name='category_detail'),
    # path('<str:pk>', PostOfCategoryAPI.as_view(), name='store_search'),

    path('login', LoginAPI.as_view(), name='login'),
    path('register', RegisterAPI.as_view(), name='register'),
    path('admin/', include('app.api_views.admin.urls')),
    path('user/', include('app.api_views.user.urls')),
]
