import jwt
from rest_framework import authentication, exceptions
from app.models.user import User, NONE_USER
from app.utils import jwt_util
from django.utils.translation import ugettext_lazy as _

from app.utils.constants import TOKEN_TYPE, ERROR_MESSAGE


class JwtAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        is_cookie = False
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            jwt_value = request.COOKIES.get('access_token')
            is_cookie = True
            if jwt_value is None:
                return (NONE_USER, None)

        try:
            payload = jwt_util.extract_payload(jwt_value)
        except jwt.ExpiredSignatureError:
            if is_cookie:
                return (NONE_USER, None)
            msg = ERROR_MESSAGE.TOKEN_EXPIRED
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError as e:
            print(str(e))
            if is_cookie:
                return (NONE_USER, None)
            msg = ERROR_MESSAGE.TOKEN_DECODING_ERROR
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            if is_cookie:
                return (NONE_USER, None)
            raise exceptions.AuthenticationFailed()
        if payload.get('type') != TOKEN_TYPE.ACCESS:
            raise exceptions.AuthenticationFailed(ERROR_MESSAGE.TOKEN_WRONG_TYPE_ACCESS)

        user = self.authenticate_credentials(payload)

        return (user, payload)

    def get_jwt_value(self, request):
        # print("\n")
        # print(request.META)
        # print("\n")
        # for key in request.META.keys():
        #     print(key, request.META.get(key))
        if len(authentication.get_authorization_header(request)) == 0:
            # print("length auth = 0")
            return None
        # print(authentication.get_authorization_header(request))
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
