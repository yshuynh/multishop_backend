import datetime
from server import settings
import jwt


def extract_token(user):
    payload = {
        'id': user.id,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.now()
    }

    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token


def extract_payload(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
