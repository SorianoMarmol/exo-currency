from django.core.exceptions import ImproperlyConfigured
# from django.utils.importlib import import_module
from importlib import import_module


def get_connection(path=None):
    try:
        mod_name, klass_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except ImportError as e:
        raise ImproperlyConfigured(
            ('Error importing provider adapter backend module %s: "%s"'
             % (mod_name, e)))
    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise ImproperlyConfigured(('Module "%s" does not define a '
                                    '"%s" class' % (mod_name, klass_name)))
    return klass()
