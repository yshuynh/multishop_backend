from django.contrib.auth.middleware import AuthenticationMiddleware
from rest_framework import exceptions

from app.authentication import JwtAuthentication
from app.models import NONE_USER


class CustomAuthMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        try:
            jwt_auth = JwtAuthentication()
            request.user, _ = jwt_auth.authenticate(request)
        except exceptions.AuthenticationFailed as e:
            request.user = NONE_USER
