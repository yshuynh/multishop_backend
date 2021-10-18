from rest_framework import generics, status
from rest_framework.response import Response
from app.authentication import JwtAuthentication
from app.models.rating import Rating
from app.models.user import User
from app.permissions import AdminPermission
from app.serializers import UserSerializer, RatingResponseSerializer
from app.utils.constants import USER_ROLE


class UserListAPI(generics.GenericAPIView):
    queryset = User.objects
    serializer_class = UserSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (AdminPermission,)

    def get(self, request, *arg, **kwargs):
        queryset = self.get_queryset().filter(role=USER_ROLE.USER)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class AdminResponseRatingAPI(generics.GenericAPIView):
    queryset = Rating
    serializer_class = RatingResponseSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (AdminPermission,)

    def post(self, request, pk, *arg, **kwargs):
        c_rating = self.get_object()
        data = request.data.copy()
        data['rating'] = c_rating.id
        data['user'] = self.request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
