from core import LoggerMixin


class Field(LoggerMixin):

    def __init__(self, model_field):
        self.fieldname = model_field

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.to_dict()[self.fieldname]
    
    def get_value(self, db_model):
        out = db_model

        key = None

        try:
            for key in self.fieldname.split("__"):
                out = getattr(out, key)
        except:
            self.logger.exception('Невозможно получить значение атрибута', item=db_model, path=self.fieldname, key=key)
            return None

        return out


class SerializerElasticModel(object):
    """
    Позволяет динамически строить модель для эластика, по классу сериалайзера DRF
    """

    serializer_class = None
    
    def __init__(self, db_model, _dict):
        self.db_model = db_model
        self._dict = _dict

    def to_dict(self):
        return self._dict

    def get_id(self):
        return self.to_dict()["id"]

    @classmethod
    def get_value(cls, field, db_model):
        return field.get_value(db_model)

    @classmethod
    def from_item(cls, db_model):

        output = {}

        for field in cls.get_fields():
            output[field.fieldname] = cls.get_value(field, db_model)

        return cls(db_model, output)

    @classmethod
    def get_fields(cls):
        for key in cls.serializer_class().fields:
            feild = Field(key)
            yield feild
