import json

from requests.status_codes import codes

from rest_framework import generics
from rest_framework.versioning import URLPathVersioning

from django.http import HttpResponse


class ExchangeRatesVersioning(URLPathVersioning):
    default_version = 1
    allowed_versions = 1
    version_param = 'version'


class ResourceAPIRest(generics.GenericAPIView):
    public_documentation = False
    name = 'Servicio Web'
    versioning_class = ExchangeRatesVersioning

    def has_attr(self, property):
        if hasattr(self, property):
            return True
        else:
            return False

    @classmethod
    def get_extra_actions(cls):
        return []

    @staticmethod
    def bad_request_response(context, status=codes.BAD_REQUEST):
        return HttpResponse(json.dumps(context), content_type='application/json', status=status)
