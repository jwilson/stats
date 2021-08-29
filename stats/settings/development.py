from .base import *

SECRET_KEY = 'DEVELOPMENT_KEY'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres3',
        'HOST': 'localhost',
    }
}

try:
    from .local import *
except ImportError:
    pass
