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


# Run develop elastic docker run -p 9300:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.4.3
ELASTIC_CONNECTION = dict(
    hosts=["localhost:9300"]
)

ELASTIC_INDEX = "main_index"
