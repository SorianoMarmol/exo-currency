import datetime
import json

from collections import OrderedDict

from django.conf import settings
from django.shortcuts import render

from exchange_rates.backends.base import BaseExchangeProviderBackend

from .fusioncharts import FusionCharts


def exchange_rate_evolution(request):
    data = request.GET.copy() or {}
    origin_currency = data.get('origin_currency', getattr(settings, 'DEFAULT_BASE_CURRENCY')).upper()
    date_from = data.get('date_from', datetime.datetime.today().replace(day=1, month=3))
    date_to = data.get('date_to', datetime.datetime.today())
    backend = BaseExchangeProviderBackend()
    # aquí debería hacerse una consulta, no invocar a get_rates
    data = backend.get_rates(date_from=date_from, date_to=date_to, source_currency=origin_currency)
    data = sorted(data, key=lambda x: datetime.datetime.strptime(x['valuation_date'], '%Y-%m-%d'))
    dates = []
    currencies_data = {}
    for rate in data:
        dates.append(rate.get('valuation_date'))
        exchanged_currency = rate.get('exchanged_currency')
        rate_val = rate.get('rate_value')
        curr_data = currencies_data.get(exchanged_currency, [])
        curr_data.append(rate_val)
        currencies_data[exchanged_currency] = curr_data
    datasets = []
    for key, val in currencies_data.items():
        datasets.append({"seriesname": key, "data": "|".join(val)})
    dates = list(OrderedDict.fromkeys(dates))  # set(dates) break the order
    dates = "|".join(dates)  # date.strftime("%m/%d/%Y") for date in dates])
    title = origin_currency + ' Exchange Rates Evolution'
    fc_chart = FusionCharts('zoomline', 'ex1', '900', '500', 'chart-1', 'json', """{
          "chart": {
            "caption": "%(caption)s",
            "subcaption": "Click & drag on the plot area to zoom & then scroll",
            "yaxisname": "Rate",
            "xaxisname": "Date",
            "forceaxislimits": "1",
            "pixelsperpoint": "0",
            "pixelsperlabel": "30",
            "compactdatamode": "1",
            "dataseparator": "|",
            "theme": "fusion"
          },
          "categories": [
            {
              "category": "%(dates)s"
            }
          ],
          "dataset": %(datasets)s
        }""" % {'caption': title, 'dates': dates, 'datasets': json.dumps(datasets)})
    return render(request, 'exchange_rates/exchange_rates.html', {
        'chart': fc_chart.render(),
    })
