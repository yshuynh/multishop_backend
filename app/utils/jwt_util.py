import datetime

from app.utils.constants import TOKEN_TYPE
from server import settings
import jwt


def extract_token(user, token_type):
    if token_type == TOKEN_TYPE.ACCESS:
        exp = 60
    elif token_type == TOKEN_TYPE.REFRESH:
        exp = 60*24*365
    else:
        raise "Token type is not correct."
    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=exp),
        'iat': datetime.datetime.utcnow(),
        'type': token_type
    }

    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token


def extract_payload(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
