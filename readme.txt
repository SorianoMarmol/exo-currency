Toda la información será remitida vía documento


Pasos para lanzar el proyecto Django

Se recomienda usar virtualenv.

sudo apt-get install python3-venv
python3 -m venv exo_investing
cd ~/virtualenvs/exo_investing/
source exo_investing/bin/activate

Instalar dependencias

pip install -r requirements.txt


Migrar y crear super usuario

python manage.py syncdb
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser

La migración nº 2 cargará las monedas de ejemplo. Se encuentran en settings (EXAMPLE_CURRENCIES)

Lanzar servidor, acceder al panel de administración, y dar de alta los Provider (uno por cada adapter)

http://127.0.0.1:8000/admin/exchange_rates/provider/add/
Ambos deben estar activo
Se recomienda establecer en el orden primero el de Fixer




Algunos settings a destacar

FIXER_FORCE_EXCEPTION
Por defecto a False, permite forzar una excepción el Fixer para probar el siguiente Provider (poder probar como responde ante fallos, el orden, el mock, etc.)
SHOW_PROVIDER
Devolverá el provider con los datos. 
Poder ver la fuente de los datos almacenados
 RANDOM_RANGE_INIT / RANDOM_RANGE_END
Valores aleatorios para los Rates del mock

Cuando esté todo a punto, se puede acceder a http://127.0.0.1:8000/api/v1/currency_rates/ que debe devolver los datos del día.
