from audioop import reverse

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from app.exceptions import ClientException
from app.models import User
from app.serializers import LoginSerializer


class MainPageAPI(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        print(request.get_full_path())
        list_file = ['asset-manifest.json', 'favicon.ico', 'logo192.png', 'logo512.png', 'manifest.json', 'robots.txt']
        file_name = request.get_full_path()[1:]
        if file_name in list_file:
            return redirect(f'static/public/{file_name}')
        return Response(template_name='index.html')


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
