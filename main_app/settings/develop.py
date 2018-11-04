from main_app.settings.base_settings import *


DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'elastic_db',
            'USER': 'postgres',
            'HOST': 'localhost',
            'PORT': '5433',
        }
}
