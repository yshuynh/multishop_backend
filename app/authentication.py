import jwt
from rest_framework import authentication, exceptions
from rest_framework_jwt.settings import api_settings
from app.models.user import User, NONE_USER
from app.utils import jwt_util


class JwtAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return (NONE_USER, None)

        try:
            payload = jwt_util.extract_payload(jwt_value)
        except jwt.ExpiredSignatureError:
            msg = 'Signature has expired.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError as e:
            print(str(e))
            msg = 'Error decoding signature.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()
        user = self.authenticate_credentials(payload)

        return (user, payload)

    def get_jwt_value(self, request):
        if len(authentication.get_authorization_header(request)) == 0:
            return None
        auth = authentication.get_authorization_header(request).split()
        if auth[0] != b'Bearer':
            msg = 'Invalid Authorization header. Start with Bearer'
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = 'Invalid Authorization header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid Authorization header. Credentials string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        if not auth[1] or auth[1] == 0:
            msg = 'Invalid Authorization header.'
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_credentials(self, payload):
        user_id = payload.get('id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            msg = 'Invalid payload.'
            # return NONE_USER
            raise exceptions.AuthenticationFailed(msg)
        return user
