Toda la información se encuentra en: "Documentación_ExoCurrency_v1.pdf"


Pasos para lanzar el proyecto Django

Se recomienda usar virtualenv.

1) crear virtualenv

sudo apt-get install python3-venv
python3 -m venv exo_investing

2) una vez creado, localizar el activate para activarlo y comenzar a trabajar

cd ~/virtualenvs/exo_investing/
source exo_investing/bin/activate


Instalar dependencias

pip install -r requirements.txt

Hay un warning que no afecta para poder trabajar, es el siguiente:

Building wheels for collected packages: unicode-slugify
 Running setup.py bdist_wheel for unicode-slugify ... error
 Complete output from command /home/rsoriano/exo_investing/bin/python3 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-suh28xwu/unicode-slugify/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" bdist_wheel -d /tmp/tmpcf03ufmnpip-wheel- --python-tag cp35:
 usage: -c [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
    or: -c --help [cmd1 cmd2 ...]
    or: -c --help-commands
    or: -c cmd --help
 
 error: invalid command 'bdist_wheel'
 
 ----------------------------------------
 Failed building wheel for unicode-slugify
 Running setup.py clean for unicode-slugify

No afecta para trabajar y si se vuelve a ejecutar el pip install no vuelve a aparecer


Migrar y crear super usuario

Dentro de la carpeta exo-currency

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
