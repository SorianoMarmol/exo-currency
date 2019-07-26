import logging
import datetime
import json
import requests


from decimal import Decimal
from functools import reduce

from django.conf import settings
from django.db.models.query import QuerySet

from exchange_rates.models import CurrencyExchangeRate, Currency, Provider
from exchange_rates.utils import get_day_list, get_exchange_rate_data

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class BaseExchangeProviderBackend(object):
    name = None
    url = None
    code = None

    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date, provider=None, *args, **kwargs):
        """Return list of dict with exchanged_currency, rate_value, source_currency, valuation_date"""
        raise NotImplementedError

    def get_url(self, *args, **kwargs):
        """Update url with GET params."""
        raise NotImplementedError

    def get_default_params(self):
        """Default GET params."""
        return {}

    def get_response(self, url=None, **params):
        url = url if url else self.get_url(**params)
        return requests.get(url)

    def parse_json(self, response):
        if isinstance(response, bytes):
            response = response.decode("utf-8")
        return json.loads(response, parse_float=Decimal)

    @classmethod
    def _get_available_currencies(cls, values_list=None):
        if not values_list:
            return Currency.objects.all()
        return Currency.objects.values_list(values_list, flat=True if values_list == 'code' else False)

    @classmethod
    def _get_available_currencies_codes(cls, str_comma_separated=True):
        currencies = cls._get_available_currencies(values_list='code')
        codes = [currency for currency in currencies]
        if str_comma_separated:
            return ','.join(codes)
        return codes
    
    @classmethod
    def _get_rates_from_stored_data(cls, source_currency, exchanged_currency, valuation_date, provider=None):
        filters = vars().copy()
        filters.pop('cls')
        if not provider:
            filters.pop('provider')
        return CurrencyExchangeRate.objects.filter(**filters)

    @classmethod
    def _get_providers(cls, values_list=None):
        if not values_list:
            return Provider.objects.filter(active=True).order_by('order')
        return Provider.objects.filter(active=True).values_list(values_list).order_by('order')

    @classmethod
    def _get_provider(cls, index=0):
        return cls._get_providers()[index]

    @classmethod
    def _get_provider_by_code(cls, code):
        return Provider.objects.get(adapter=code)

    @classmethod
    def _get_currency_object(cls, currency_or_code):
        if not isinstance(currency_or_code, Currency):
            return Currency.objects.get(code=currency_or_code)
        return currency_or_code

    @classmethod
    def _get_currency_code(cls, currency_or_code):
        if isinstance(currency_or_code, Currency):
            return currency_or_code.code
        return currency_or_code

    @classmethod
    def parse_date_to_str(cls, date):
        if isinstance(date, datetime.date):
            date = datetime.datetime.strftime(date, "%Y-%m-%d")
        return date

    @classmethod
    def parse_date_str_to_date(cls, date):
        if not isinstance(date, datetime.date):
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
        return date

    def get_rates(self, date_from=datetime.datetime.today(), date_to=datetime.datetime.today(), source_currency=getattr(
            settings, 'DEFAULT_BASE_CURRENCY', 'EUR'), exchanged_currency=None, *args, **kwargs):
        """CurrencyExchangeRate instance or call get_exchange_rate_data ​ to retrieve data from the Provider"""
        provider = self._get_provider()
        # obtener el provider segun el orden
        # del provider sacamos el adaptador para la consulta
        data = []
        days = get_day_list(self.parse_date_str_to_date(date_from), self.parse_date_str_to_date(date_to))
        for day in days:
            if not exchanged_currency:
                exchanged_currency = self._get_available_currencies()
            elif not isinstance(exchanged_currency, list) and not isinstance(exchanged_currency, QuerySet):
                exchanged_currency = [exchanged_currency]
            for currency in exchanged_currency:
                source_currency_obj = self._get_currency_object(source_currency)
                if currency == source_currency_obj or currency == source_currency:
                    continue
                # comprobamos si está en CurrencyExchangeRate
                stored_data = self._get_rates_from_stored_data(
                    self._get_currency_object(source_currency), self._get_currency_object(currency), day)
                # si no hacemos la consulta
                if not stored_data:
                    provider_data = get_exchange_rate_data(source_currency, currency, day, provider)
                    if isinstance(provider_data, list):
                        data = data + provider_data
                    elif isinstance(provider_data, dict):
                        data.append(provider_data)
                else:
                    data.append(stored_data.get().parsed_data)
        return data

    def calculate_amount(self, origin_currency, amount, target_currency, date=datetime.datetime.today(), *args, **kwargs):
        rates = self.get_rates(date_from=date, date_to=date, source_currency=origin_currency, exchanged_currency=target_currency)
        rate = rates[0].get('rate_value')
        return str(Decimal(amount) * Decimal(rate))

    def calculate_time_weighted_rate(self, origin_currency, amount, target_currency, date_invested=datetime.datetime.today()):
        """
        Calculate TWR
        1 - Calculate the rate of return for each sub-period by subtracting the beginning balance of the period
        from the ending balance of the period and divide the result by the beginning balance of the period.
        2 -Create a new sub-period for each period that there is a change in cash flow, whether it's a withdrawal or deposit.
        You'll be left with multiple periods, each with a rate of return.
        Add 1 to each rate of return, which simply makes negative returns easier to calculate.
        3- Multiply the rate of return for each sub-period by each other. Subtract the result by 1 to achieve the TWR.
        """
        rates = self.get_rates(date_from=date_invested, source_currency=origin_currency, exchanged_currency=target_currency)
        rates_values = []
        amount_values = []
        period_values = []
        amount = Decimal(amount)
        day_amount = amount  # first day
        log.debug('Orig amount ' + str(day_amount))
        for rate in rates:
            log.debug('Comenzando con amount val ' + str(day_amount))
            rate_value = Decimal(rate.get('rate_value'))
            log.debug('Rate val ' + str(rate_value))
            rates_values.append(rate_value)
            day_value = Decimal(amount) * rate_value
            log.debug('Day val ' + str(day_value))
            amount_values.append(day_value)
            period_value = (day_value - day_amount) / day_amount
            log.debug('Period val ' + str(period_value))
            log.debug('Period val +1: =' + str(period_value + 1))
            day_amount = Decimal(day_value)  # next day, the value is the past day
            period_values.append(period_value + 1)
        twr = reduce((lambda x, y: x * y), period_values) - 1
        log.debug('result con -1: =' + str(twr))
        # considerando un periodo en vez de todos los días
        last_value = Decimal(rates[-1].get('rate_value')) * amount
        twr_one_period = (last_value - amount) / amount
        log.debug('Resultado suponiendo un periodo en vez de cada dia: ' + str(twr_one_period))
        return str(twr)
