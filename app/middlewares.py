from django.contrib.auth.middleware import AuthenticationMiddleware
from app.authentication import JwtAuthentication


class CustomAuthMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        jwt_auth = JwtAuthentication()
        request.user, _ = jwt_auth.authenticate(request)
