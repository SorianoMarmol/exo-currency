import datetime
import logging

from exchange_rates import get_connection
from exchange_rates.models import Provider

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)


def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider, provider_index=0):
    """Get exchange rate data from provider. If there is an error getting data, try with the next provider.

    Args:
        source_currency (str): source currency code
        exchanged_currency (str): exchanged currency code
        valuation_date (date): date to val
        provider (int or Provider object): provider for get the data
        provider_index (int): provider index for try recursively

    Returns:
        data  list of dict with exchanged_currency, rate_value, source_currency, valuation_date

    Raises:
        IndexError: can't not get data from any provider
    """
    if isinstance(provider, int):
        provider = Provider.objects.get(id=provider)
    connection = get_connection(provider.get_adapter_path)
    try:
        # provider is not needed due to connector
        return connection.get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider)
    except Exception as e:  # TODO; catch real exceptions
        log.error('Problem getting data from provider: %(provider)s . Exception: %(exception)s' % {'provider': provider.name, 'exception': e})
        # try another provider
        provider_index += 1
        try:
            provider = connection._get_provider(provider_index)
            return get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider, provider_index)
        except IndexError:  # no more providers
            raise Exception("Can not get data from any provider")


def get_day_list(start_date, end_date):
    """ Get a day list between two dates"""
    dates = []
    if (start_date < end_date) or (start_date == end_date):
        delta = end_date - start_date
        for i in range(delta.days + 1):
            day = start_date + datetime.timedelta(days=i)
            try:
                dates.append(day.date())
            except AttributeError:
                dates.append(day)
    return dates
