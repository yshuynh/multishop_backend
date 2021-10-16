from rest_framework import generics
from rest_framework.response import Response
from app.authentication import JwtAuthentication
from app.models.user import User
from app.serializers import UserSerializer


class UserInfoAPI(generics.GenericAPIView):
    queryset = User.objects
    serializer_class = UserSerializer
    authentication_classes = (JwtAuthentication,)

    def get(self, request, *arg, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
