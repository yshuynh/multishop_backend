ALLOWED_ID_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'


class BaseConstant:
    @classmethod
    def choices(cls):
        return [(value, value) for name, value in vars(cls).items() if name.isupper()]


class USER_ROLE(BaseConstant):
    ADMIN = 'admin'
    USER = 'user'
