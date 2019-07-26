#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Import CurrencyExchangeRate data from CSV file
"""
import csv
from decimal import Decimal


from django.core.management.base import BaseCommand, CommandError
try:
    from django.utils.encoding import force_unicode
except:
    from django.utils.encoding import force_text as force_unicode

from exchange_rates.models import CurrencyExchangeRate, Currency


def ask_for_confirmation(prompt, prompt_sufix=' (y/n)[n]: '):
    answer = input(prompt + prompt_sufix).strip()
    if not answer:
        return False
    if answer == '':
        return False
    elif answer not in ('y', 'n', 'yes', 'no'):
        print ('Please answer yes or no')
    elif answer.lower() == 'y' or answer.lower() == 'yes':
        return True
    else:
        return False

# easy change csv header data, or add more fields
# key = field, value = csv header
CSV_MAP = {
    'source_currency': 'SOURCE CURRENCY',
    'exchanged_currency': 'EXCHANGED CURRENCY',
    'valuation_date': 'VALUATION DATE',
    'rate_value': 'RATE',
}


class Command(BaseCommand):
    help = 'Import CurrencyExchangeRate data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='CSV File', type=str)
        parser.add_argument(
            '-y', '--yes', action='store_true',
            dest='assume_yes', help="Assume YES on all questions")
        parser.add_argument(
            '-e', '--encoding', dest='encoding',
            default='utf8', help='Encoding (default UTF8)')

    def get_field(self, row, field):
        value = row.get(CSV_MAP[field], '').strip()
        # return force_unicode(value.decode(self.encoding))
        return force_unicode(value)

    def clean_characters(self, value):
        """ Clean or fix CSV values, if needed """
        return value

    def _check_currency(self, code):
        try:
            return Currency.objects.get(code=code.upper())
        except Currency.DoesNotExist:
            raise CommandError('Cuerrency does not exist or is not available')

    def handle(self, *args, **options):
        assume_yes = options.get('assume_yes', False)

        if not assume_yes and not ask_for_confirmation('Do you want to import CurrencyExchangeRate data?'):
            return

        self.encoding = options['encoding']
        csv_file = options.get('csv_file')

        csv_file = open(csv_file, 'r')
        reader = csv.DictReader(csv_file, skipinitialspace=True, delimiter=';', quoting=csv.QUOTE_NONE)

        for i, field_name in enumerate(reader.fieldnames):
            reader.fieldnames[i] = field_name.strip()

        for row in reader:
            source_currency = self._check_currency(
                self.clean_characters(self.get_field(row, 'source_currency')))
            exchanged_currency = self._check_currency(self.clean_characters(
                self.get_field(row, 'exchanged_currency')))
            valuation_date = self.clean_characters(self.get_field(row, 'valuation_date'))
            rate_value = Decimal(self.clean_characters(self.get_field(row, 'rate_value')))
            CurrencyExchangeRate.objects.get_or_create(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency, rate_value=rate_value,
                valuation_date=valuation_date)
