from django.conf import settings
from django.shortcuts import render

from .models import Currency, CurrencyExchangeRate


def exchange_rate_evolution(request, base=getattr(settings, 'DEFAULT_BASE_CURRENCY'), target='USD', months=6):
    available_currencies = Currency.objects.all()
    base_currency = available_currencies.get(code=base)
    rates = CurrencyExchangeRate.objects.all()
    base_rate = CurrencyExchangeRate.objects.filter(source_currency__code=base).select_related().first()
    return render(request, 'exchange_rates/exchange_rates.html', {
        "base_currency": base_currency, 'currencies': available_currencies,
        'base_currency_code': base,
        'target_currency_code': target,
        'base_rate': base_rate,
        'rates': rates,
    })
