import datetime
import json
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status

from django.http import HttpResponse

from exchange_rates.api_rest import ResourceAPIRest
from exchange_rates.backends.base import BaseExchangeProviderBackend


class CurrencyRatesWS(ResourceAPIRest):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    # public_documentation = True
    group = 'Currency Rates WS'
    name = 'CurrencyRates'
    code = 'CurrencyRates'
    # url_documentation = 'CurrencyRates'

    # def get_serializer_class(self):
    #     if self.request.version == 'v1':
    #         return ExampleSerializerV1
    #     return ExampleSerializer

    def get(self, request, *args, **kwargs):
        data = request.GET.copy() or {}
        date_from = data.get('date_from', datetime.datetime.today())
        date_to = data.get('date_to', datetime.datetime.today())
        backend = BaseExchangeProviderBackend()
        data = backend.get_rates(date_from=date_from, date_to=date_to)
        return HttpResponse(json.dumps(data), content_type='application/json', status=status.HTTP_200_OK)


class CalculateAmountWS(ResourceAPIRest):
    group = 'CalculateAmount WS'
    name = 'CalculateAmount'
    code = 'CalculateAmount'
    REQUIRED_PARAMS = ['origin_currency', 'amount', 'target_currency']

    def get(self, request, *args, **kwargs):
        data = request.GET.copy() or {}
        for key in self.REQUIRED_PARAMS:
            if key not in data.keys():
                return self.bad_request_response({'ERROR': 'Invalid data received'})
        origin_currency = data.get('origin_currency').upper()
        amount = data.get('amount')
        if ',' in amount:
            amount = amount.replace(',', '.')
        target_currency = data.get('target_currency').upper()
        backend = BaseExchangeProviderBackend()
        data = backend.calculate_amount(origin_currency, amount, target_currency)
        return HttpResponse(json.dumps(data), content_type='application/json', status=status.HTTP_200_OK)


class TimeWeightedRateWS(ResourceAPIRest):
    group = 'TimeWeightedRate W'
    name = 'TimeWeightedRate'
    code = 'TimeWeightedRate'
    REQUIRED_PARAMS = ['origin_currency', 'amount', 'target_currency', 'date_invested']

    def get(self, request, *args, **kwargs):
        data = request.GET.copy() or {}
        for key in self.REQUIRED_PARAMS:
            if key not in data.keys():
                return self.bad_request_response({'ERROR': 'Invalid data received'})
        origin_currency = data.get('origin_currency').upper()
        amount = data.get('amount')
        if ',' in amount:
            amount = amount.replace(',', '.')
        target_currency = data.get('target_currency').upper()
        date_invested = data.get('date_invested', datetime.datetime.today())
        backend = BaseExchangeProviderBackend()
        data = backend.calculate_time_weighted_rate(origin_currency, amount, target_currency, date_invested)
        return HttpResponse(json.dumps(data), content_type='application/json', status=status.HTTP_200_OK)
