from rest_framework import serializers, mixins
from rest_framework.viewsets import GenericViewSet

from flats.models import Flat


class FlatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flat
        fields = '__all__'


class FlatListViewSet(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin):
    serializer_class = FlatSerializer
    queryset = Flat.objects.all()
