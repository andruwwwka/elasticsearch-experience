class Field(object):

    def __init__(self, model_field):
        self.model_field = model_field


class SerializerElasticModel(object):
    """
    Позволяет динамически строить модель для эластика, по классу сериалайзера DRF
    """

    serializer_class = None

    @classmethod
    def get_fields(cls):
        for key in cls.serializer_class().fields:
            feild = Field(key)
            feild.fieldname = key
            yield feild
