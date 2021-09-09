from .base import *

DEBUG = False

SECRET_KEY = 'PRODUCTION_KEY'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres',
        'PORT': 5432,

    }
}

try:
    from .local import *
except ImportError:
    pass
