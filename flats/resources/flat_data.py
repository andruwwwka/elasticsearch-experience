from rest_framework import serializers, mixins
from rest_framework.viewsets import GenericViewSet

from flats.models import Flat


class FlatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flat


class FlatListViewSet(GenericViewSet,
                      mixins.ListModelMixin):
    serializer_class = FlatSerializer
