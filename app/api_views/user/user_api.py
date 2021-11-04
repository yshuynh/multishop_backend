from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from app.authentication import JwtAuthentication
from app.models.rating import Rating
from app.models.user import User
from app.permissions import UserPermission, LoggedPermission
from app.serializers import UserSerializer, UserInfoSerializer, UserRateProductSerializer, RatingResponseSerializer


class UserInfoAPI(generics.GenericAPIView):
    queryset = User.objects
    serializer_class = UserSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UserInfoSerializer
        return UserSerializer

    def get(self, request, *arg, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def put(self, request, *arg, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRateProductAPI(generics.GenericAPIView):
    queryset = User.objects
    serializer_class = UserRateProductSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission,)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        user_id = request.user.id
        product_id = request.data.get('product')
        data['is_solved'] = False
        try:
            rating = Rating.objects.get(user=user_id, product_id=product_id)
            serializer = self.get_serializer(rating, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rating.DoesNotExist:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResponseRatingAPI(generics.GenericAPIView):
    queryset = Rating
    serializer_class = RatingResponseSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (LoggedPermission,)

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