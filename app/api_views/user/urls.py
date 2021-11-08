from django.urls import path, include
from app.api_views.user.user_api import *

urlpatterns = [
    path('me', UserInfoAPI.as_view(), name='user_info'),
    path('ratings', UserRateProductAPI.as_view(), name='user_rate'),
    path('ratings/<str:pk>/response', UserResponseRatingAPI.as_view(), name='user_response_rating'),
    path('carts', UserCartListAPI.as_view(), name='user_cart_list'),
    path('carts/add', UserCartAddItemAPI.as_view(), name='user_cart_add'),
    path('carts/remove', UserCartRemoveItemAPI.as_view(), name='user_cart_remove'),
    # path('carts/<str:pk>', UserCartItemSingleAPI.as_view(), name='user_cart_single'),

    path('orders', UserOrderListAPI.as_view(), name='user_order_list'),
]
