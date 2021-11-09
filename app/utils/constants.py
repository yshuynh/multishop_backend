ALLOWED_ID_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
SHIPPING_FEE = 30000


class BaseConstant:
    @classmethod
    def choices(cls):
        return [(value, value) for name, value in vars(cls).items() if name.isupper()]

    def next_state(self, state):
        list_value = [value for name, value in vars(self).items() if name.isupper()]
        for i in range(0, len(list_value) - 1):
            if list_value[i] == state:
                return list_value[i + 1]
        return None


class USER_ROLE(BaseConstant):
    ADMIN = 'admin'
    USER = 'user'


class TOKEN_TYPE(BaseConstant):
    ACCESS = 'access'
    REFRESH = 'refresh'


class ORDER_STATUS(BaseConstant):
    WAITING_CONFIRM = 'waiting_confirm'
    CONFIRMED = 'confirmed'
    SHIPPING = 'shipping'
    SUCCESS = 'success'


# class PAYMENT_TYPE(BaseConstant):
#     CASH = 'cash'
#     MOMO = 'momo'


class ERROR_MESSAGE(BaseConstant):
    TOKEN_EXPIRED = 'Signature has expired.'
    TOKEN_DECODING_ERROR = 'Error decoding signature.'
    TOKEN_WRONG_TYPE_ACCESS = 'Use access_token instead of refresh_token.'
    TOKEN_WRONG_TYPE_REFRESH = 'Use refresh_token instead of access_token.'
