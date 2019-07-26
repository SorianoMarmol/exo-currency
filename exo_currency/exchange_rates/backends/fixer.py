import datetime

from dateutil.parser import parse

from django.conf import settings

from exchange_rates.models import CurrencyExchangeRate

from .base import BaseExchangeProviderBackend


class FixerExchangeProviderBackend(BaseExchangeProviderBackend):
    name = getattr(settings, 'FIXER_ADAPTER_CODE', 'FIXER')
    url = getattr(settings, 'FIXER_ADAPTER_URL', 'http://data.fixer.io/api/latest')
    code = getattr(settings, 'FIXER_ADAPTER_CODE', 'FIXER')
    access_key = getattr(settings, 'FIXER_ACCESS_KEY', 'b3b31808333471c81e10b1f851d1a1b3')

    def get_url(self, base, symbols, valuation_date=None):
        """Update url with GET params."""
        url = self.url + "?access_key=" + self.access_key + "&base=" + base + "&symbols=" + symbols
        if valuation_date:
            if isinstance(valuation_date, datetime.date):
                if valuation_date == datetime.datetime.today():
                    return url  # avoid query historical
                valuation_date = datetime.datetime.strftime(valuation_date, "%Y-%m-%d")
            # elif isinstance(valuation_date, str):
            #     valuation_date = datetime.datetime.strptime(valuation_date, "%Y-%m-%d")
            url = url.replace('latest', str(valuation_date))
        return url

    def parse_response(self, response):
        data = self.parse_json(response.text)
        data.pop('success', '')
        data.pop('timestamp', '')
        data.pop('historical', '')
        # settings mapping?
        data['source_currency'] = data.pop('base')
        data['valuation_date'] = parse(data.pop('date')).date()
        return data

    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date=datetime.datetime.today(), provider=None):
        """Return list of dict with exchanged_currency, rate_value, source_currency, valuation_date"""
        # provider is not needed due to connector
        if provider and provider.adapter != self.code:  # testing purposes
            raise Exception()
        # forzar excepción para siguiente backend (pruebas)
        if getattr(settings, 'FIXER_FORCE_EXCEPTION', False):
            raise Exception('prueba con el siguiente adapter')
        source_currency = self._get_currency_code(source_currency)
        exchanged_currency = self._get_currency_code(exchanged_currency)
        response = self.get_response(url=self.get_url(base=source_currency, symbols=exchanged_currency, valuation_date=valuation_date,))
        parsed_response = self.parse_response(response)
        rates = parsed_response.get('rates')
        valuation_date = parsed_response.get('valuation_date')
        data = []
        for currency_code, val in rates.items():
            currency, __ = CurrencyExchangeRate.objects.get_or_create(
                source_currency=self._get_currency_object(source_currency),
                exchanged_currency=self._get_currency_object(currency_code), rate_value=val,
                valuation_date=valuation_date, provider=self._get_provider_by_code(self.code))
            data.append(currency.parsed_data)
        return data
