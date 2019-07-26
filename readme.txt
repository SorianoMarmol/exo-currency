NOTAS INTERNAS
* https://stackoverflow.com/questions/54168569/show-resulting-json-from-api-in-simple-django-template

* Create project + app
django-admin startproject exo_currency
cd exo_currency/
django-admin startapp exchange_rates

python manage.py migrate
python manage.py createsuperuser --email sorianomarmol@gmail.com --username admin

python manage.py makemigrations



* Create virtual env

sudo apt-get install python3-venv
python3 -m venv exo_investing

* Activate virtual env

cd ~/virtualenvs/exo_investing/
source exo_investing/bin/activate

* Requirements

Django~=2.0.13
djangorestframework==3.10.0
requests==2.22.0
pytest-django==3.5.1
  pytest==5.0.1
django-categories==1.6.1
python-dateutil==2.8.0

pip install -r requirements.txt

* example currencies

Before first migrate:

You can override EXAMPLE_CURRENCIES in settings.py 
EXAMPLE_CURRENCIES = {
    "EUR": "Euro",
    "USD": "Dollar(US)",
    "GBP": "Pound sterling",
    "BRL": "Brazilian real"
}


python manage.py migrate
python manage.py createsuperuser 

* runserver, login, and set the Providers:
** http://127.0.0.1:8000/admin/exchange_rates/provider/add/

* Pruebas básicas

Para realizar las pruebas, se puede usar cualquier backend/adapter ya que siempre da prioridad al orden y lo intenta con todos

In [3]: from exchange_rates.backends.fixer import * 
   ...: backend = FixerExchangeProviderBackend() 
   ...:  
   ...:  
   ...: backend.get_rates(source_currency='CHF', exchanged_currency='USD', date_from = '2019-07-14')

con el propio base también se puede probar

In [4]: from exchange_rates.backends.base import *
In [5]: backend = BaseExchangeProviderBackend()
In [6]: backend.get_rates(source_currency='CHF', exchanged_currency='USD', date_from = '2019-07-13')   