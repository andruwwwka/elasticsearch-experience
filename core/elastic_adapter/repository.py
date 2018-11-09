import json
from multiprocessing.pool import ThreadPool

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

    def _create(self):
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

    def _drop(self):
        try:
            self.connection.indices.delete(
                index=self.index
            )
        except Exception as e:
            self.logger.warning('Невозможно удалить индекс: {} ({})'.format(self.index, e))

    def recreate(self):
        self.logger.info('Пересоздание индекса {}'.format(self.index))
        self._drop()
        self._create()

    def _index_dict(self, elastic_model):
        self.connection.index(
            index=self.index,
            doc_type=self.doc_type,
            id=elastic_model.get_id(),
            body=elastic_model.to_dict()
        )

    def reindex_one(self, item):
        try:
            elastic_model = self.model.from_item(item, )
            self._index_dict(elastic_model)
        except Exception:
            self.logger.exception('Невозможно реиндексировать элемент %s', item)

    def reindex_items(self, items):
        try:
            pool = ThreadPool(50)
            pool.map(
                self.reindex_one,
                items
            )
            pool.terminate()
        except Exception:
            self.logger.exception('Невозможно индексировать элементы')

    def delete_index(self, items):
        qs = list(items)

        pool = ThreadPool(10)

        def _worker(item):
            try:
                self.connection.delete(
                    index=self.index,
                    doc_type=self.doc_type,
                    id=item.id
                )
            except Exception:
                self.logger.exception(
                    'Невозможно удаление элемента',
                    id=item.id,
                    index=self.index,
                    doc_type=self.doc_type
                )

        pool.map(_worker, qs)
        pool.terminate()

    def _get_mapping(self):
        if self._mapping is None:
            self._mapping = self.connection.indices.get_mapping(
                index=self.index,
                doc_type=self.doc_type
            ).get(self.index, {}).get('mappings', {}).get(self.doc_type, {}).get('properties', {})

        return self._mapping

    def _parse_query_items(self, filters):
        out = {
            "bool": {
                "must": []
            }
        }

        for key, value in filters.items():
            if key.replace("__in", "") in self._get_mapping():
                if key.endswith("__in"):
                    out["bool"]["must"].append({
                        "terms": {
                            key.replace("__in", ""): value
                        }
                    })
                else:
                    out["bool"]["must"].append({
                        "term": {
                            key: value
                        }
                    })

        return out

    def _build_aggregation_items(self, fields):
        out = {}
        for key in fields:
            if key in self._get_mapping():
                out[key] = {
                    "terms": {
                        "field": key,
                        "size": 10000
                    }
                }

        return out

    def get_filters(self, fields, filters):
        body = {
            'size': 0,
            'query': self._parse_query_items(filters),
            'aggs': self._build_aggregation_items(fields)
        }

        self.logger.info(
            'Запрос к эластику: index={index}; doc_type={doc_type}; body={body}'.format(
                body=json.dumps(body, indent=4),
                doc_type=self.doc_type,
                index=self.index
            )
        )

        response = self.connection.search(
            index=self.index,
            doc_type=self.doc_type,
            body=body
        )

        out = {}

        for key, data in response.get('aggregations', {}).iteritems():
            out[key] = sorted([
                item['key']
                for item in data['buckets']
            ])

        return out
