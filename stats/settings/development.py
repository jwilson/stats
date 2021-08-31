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
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     # 'NAME': BASE_DIR / 'db.sqlite3',
    #     'NAME': BASE_DIR + '/db.sqlite3',
    # }
}

try:
    from .local import *
except ImportError:
    pass
