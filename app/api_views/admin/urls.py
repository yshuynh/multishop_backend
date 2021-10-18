from django.urls import path
from app.api_views.admin.admin_api import *

urlpatterns = [
    path('users', UserListAPI.as_view(), name='admin_user_list'),
    path('<str:pk>/response', AdminResponseRatingAPI.as_view(), name='admin_response_rating'),
]
