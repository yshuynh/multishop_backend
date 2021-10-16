from rest_framework import generics, status
from rest_framework.response import Response
from app.authentication import JwtAuthentication
from app.models.user import User
from app.serializers import UserSerializer, UserInfoSerializer


class UserInfoAPI(generics.GenericAPIView):
    queryset = User.objects
    serializer_class = UserSerializer
    authentication_classes = (JwtAuthentication,)

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
