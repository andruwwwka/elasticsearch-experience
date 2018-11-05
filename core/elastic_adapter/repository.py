from django.conf import settings
from elasticsearch import client

from core import LoggerMixin
from core.elastic_adapter.model import SerializerElasticModel


class ElasticRepository(LoggerMixin):
    """
    Класс, предоставляющие модели методы для работы с репозиторием эластика
    """

    model = None

    doc_type = None

    def __init__(self, model, doc_type):
        assert model and issubclass(model, SerializerElasticModel), 'Неверная модель: {}'.format(model)
        self.model = model
        self.doc_type = doc_type
        self.connection = client.Elasticsearch(
            **settings.ELASTIC_CONNECTION
        )
        self.index = settings.ELASTIC_INDEX
        self._mapping = None

    def create(self):
        try:
            self.connection.indices.create(
                self.index,
                body={
                    'mappings': {
                        '_default_': {
                            'dynamic_templates': [
                                {
                                    'string': {
                                        'mapping': {
                                            'index': 'not_analyzed',
                                            'type': 'keyword'
                                        },
                                        'match_mapping_type': 'string'
                                    }
                                }
                            ]
                        }
                    }
                }
            )
            self.logger.info('Создан индекс {}'.format(self.index))
        except Exception:
            self.logger.warning('Индекс {} уже существует!'.format(self.index))

    def recreate(self):
        self.logger.info('Пересоздание индекса {}'.format(self.index))

        try:
            self.connection.indices.delete(
                self.index
            )
        except Exception as e:
            self.logger.warning('Невозможно удалить индекс: {} ({})'.format(self.index, e))

        self.create()
