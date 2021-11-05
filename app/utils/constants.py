ALLOWED_ID_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'


class BaseConstant:
    @classmethod
    def choices(cls):
        return [(value, value) for name, value in vars(cls).items() if name.isupper()]


class USER_ROLE(BaseConstant):
    ADMIN = 'admin'
    USER = 'user'


class TOKEN_TYPE(BaseConstant):
    ACCESS = 'access'
    REFRESH = 'refresh'


class ERROR_MESSAGE(BaseConstant):
    TOKEN_EXPIRED = 'Signature has expired.'
    TOKEN_DECODING_ERROR = 'Error decoding signature.'
    TOKEN_WRONG_TYPE_ACCESS = 'Use access_token instead of refresh_token.'
    TOKEN_WRONG_TYPE_REFRESH = 'Use refresh_token instead of access_token.'
