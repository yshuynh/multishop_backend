from rest_framework import exceptions, status
from django.utils.translation import ugettext_lazy as _
from server import settings


class ClientException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'default'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = {
            'detail': detail,
            'code': code
        }

