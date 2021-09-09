from .base import *

SECRET_KEY = 'DEVELOPMENT_KEY'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': 5432,

    }
}

try:
    from .local import *
except ImportError:
    pass
