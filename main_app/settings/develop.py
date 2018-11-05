from .base_settings import *

# Run develop database docker run -e POSTGRES_DB=elastic_db -p 5433:5432 postgres
DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'elastic_db',
            'USER': 'postgres',
            'HOST': 'localhost',
            'PORT': '5433',
        }
}
