# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status

from django.http import HttpResponse

from exchange_rates.api_rest import ResourceAPIRest


class CurrencyRatesWS(ResourceAPIRest):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    # public_documentation = True
    group = 'Currency Rates WS'
    name = 'Currency Rates'
    code = 'CurrencyRates'
    # url_documentation = 'CurrencyRates'

    # def get_serializer_class(self):
    #     if self.request.version == 'v1':
    #         return ExampleSerializerV1
    #     return ExampleSerializer

    def get(self, request, *args, **kwargs):
        data = request.GET.copy() or {}
        st = None
        return HttpResponse(data, content_type='application/json', status=st or status.HTTP_200_OK)
