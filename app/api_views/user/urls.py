from django.urls import path, include
from app.api_views.user.user_api import *

urlpatterns = [
    path('me', UserInfoAPI.as_view(), name='user_info'),
    path('rating', UserRateProductAPI.as_view(), name='user_rate'),
    path('rating/<str:pk>/response', UserResponseRatingAPI.as_view(), name='user_response_rating'),
]
