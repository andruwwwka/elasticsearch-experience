from django.db.models.signals import post_delete, post_save
from django.dispatch import Signal, receiver

from core.elastic_adapter.repository import ElasticRepository


queryset_changed = Signal(providing_args=["qs"])


queryset_deleted = Signal(providing_args=["qs"])


@receiver(post_delete)
def listen_post_delete_queryset_deleted(sender, instance, **k):
    queryset_deleted.send(
        sender=sender,
        qs=[instance]
    )


@receiver(post_save)
def listen_post_save_emit_queryset_changed(sender,  instance, **k):
    queryset_changed.send(
        sender=sender,
        qs=[instance]
    )


@receiver(queryset_changed)
def listen_queryset_changed(sender, qs, **kwargs):
    SignalHandler.on_change(sender, qs)


@receiver(queryset_deleted)
def listen_queryset_deleted(sender, qs, **kwargs):
    SignalHandler.on_delete(sender, qs)


class _InitialIndex(object):
    repository = None
    queryset = None

    def __init__(self, **k):
        self.__dict__.update(k)


class _HandlerItem(object):
    repository = None
    idGetterFunction = None

    def __init__(self, **k):
        self.__dict__.update(k)

    def __hash__(self):
        return hash(self.repository) + hash(self.idGetterFunction)


class _SignalHandler(object):
    _handlers = {}
    _initial_indexes = set()

    def initial_index(self, repository, qs):
        assert isinstance(repository, ElasticRepository)
        self._initial_indexes.add(_InitialIndex(
            repository=repository,
            queryset=qs
        ))

        return self

    def _register_one(self, sender, repository, idGetterFunction):
        idGetterFunction = idGetterFunction or (lambda qs: qs)

        self._handlers.setdefault(sender, set()).add(_HandlerItem(
            repository=repository,
            idGetterFunction=idGetterFunction
        ))

        return self

    def register(self, sender, repository, idGetterFunction=None):
        if isinstance(sender, list):
            for s in sender:
                self._register_one(s, repository, idGetterFunction)
        else:
            self._register_one(sender, repository, idGetterFunction)

        return self

    def on_delete(self, sender, qs):
        handlers = self._handlers.get(sender, [])
        for handler in handlers:
            handler.repository.delete_index(handler.idGetterFunction(qs))

    def on_change(self, sender, qs):
        handlers = self._handlers.get(sender, [])
        for handler in handlers:
            handler.repository.reindex_items(handler.idGetterFunction(qs))


SignalHandler = _SignalHandler()
