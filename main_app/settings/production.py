from .base_settings import *


DEBUG = False

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'elastic_db',
            'USER': 'postgres',
            'HOST': 'db',
            'PORT': '5432',
        }
}
