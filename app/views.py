from audioop import reverse

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from app.exceptions import ClientException
from app.models import User
from app.serializers import LoginSerializer


class LogoutAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponseRedirect('/admin')
        response.delete_cookie('access_token')
        response.delete_cookie('sessionid')
        return response


class AdminPageLoginAPI(generics.GenericAPIView):
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
        response = HttpResponseRedirect('/admin')
        response.set_cookie('access_token', serializer.data.get('access_token'))
        return response
