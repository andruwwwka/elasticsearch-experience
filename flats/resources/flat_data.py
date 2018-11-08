from rest_framework import serializers, mixins
from rest_framework.viewsets import GenericViewSet

from core.elastic_adapter.mixins import ElasticFilterMixin
from core.elastic_adapter.model import SerializerElasticModel
from core.elastic_adapter.repository import ElasticRepository
from flats.models import Flat


class FlatSerializer(serializers.ModelSerializer):
    """
    Сериалайзер квартир
    """

    class Meta:
        model = Flat
        fields = '__all__'


class FlatElasticModel(SerializerElasticModel):
    """
    Эластик модель квартир на основе сериалайзера
    """

    serializer_class = FlatSerializer


flat_repository = ElasticRepository(
    model=FlatElasticModel,
    doc_type="flat"
)


class FlatListViewSet(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      ElasticFilterMixin):
    """
    Клиентский ресурс для получения данных о квартирах
    """

    serializer_class = FlatSerializer
    queryset = Flat.objects.all()


SignalHandler.initial_index(
    flat_repository, Flat.objects.all()
).register(
    Flat, flat_repository
)
