import datetime
import random

from dateutil.parser import parse

from django.conf import settings

from exchange_rates.models import CurrencyExchangeRate

from .base import BaseExchangeProviderBackend


class MockExchangeProviderBackend(BaseExchangeProviderBackend):
    name = getattr(settings, 'MOCK_ADAPTER_CODE', 'MOCK')
    code = getattr(settings, 'MOCK_ADAPTER_CODE', 'MOCK')

    def _generate_mock_data(self, source_currency, exchanged_currency, valuation_date):
        if isinstance(valuation_date, str):
            valuation_date = parse(valuation_date).date()
        range_init = getattr(settings, 'RANDOM_RANGE_INIT', 0.2)
        range_end = getattr(settings, 'RANDOM_RANGE_END', 1.8)
        rate_value = 1 if source_currency == exchanged_currency else random.uniform(range_init, range_end)
        return {
            'exchanged_currency': exchanged_currency,
            'rate_value': rate_value,
            'source_currency': source_currency,
            'valuation_date': valuation_date}

    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date=datetime.datetime.today(), provider=None):
        """Return list of dict with exchanged_currency, rate_value, source_currency, valuation_date"""
        # provider is not needed due to connector
        if provider and provider.adapter != self.code:  # testing purposes
            raise Exception()
        source_currency = self._get_currency_code(source_currency)
        exchanged_currency = self._get_currency_code(exchanged_currency)
        parsed_response = self._generate_mock_data(source_currency, exchanged_currency, valuation_date=valuation_date,)
        rate_value = parsed_response.get('rate_value')
        valuation_date = parsed_response.get('valuation_date')
        data = []
        currency, __ = CurrencyExchangeRate.objects.get_or_create(
            source_currency=self._get_currency_object(source_currency),
            exchanged_currency=self._get_currency_object(exchanged_currency), rate_value=rate_value,
            valuation_date=valuation_date, provider=self._get_provider_by_code(self.code))
        data.append(currency.parsed_data)
        return data
