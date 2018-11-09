from rest_framework.decorators import list_route
from rest_framework.response import Response

from core.elastic_adapter.controllers import SimpleController


class ElasticFilterMixin(object):
    """
    Предоставление ресурсу DRF методов работы с моделью эластика
    """

    controller = None

    es_filters = None

    @list_route(methods=['GET'])
    def filters(self, request):
        return Response(
            self.controller.get_filters(self.es_filters, request.query_params)
        )
