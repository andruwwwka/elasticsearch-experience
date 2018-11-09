class SimpleController(object):
    """
    Контроллер для общения с эластиком и преобразования полученных данных для обработки методами DRF
    """

    repository = None

    def __init__(self, repository):
        self.repository = repository

    def get_filters(self, fields, query_params):
        return self.repository.get_filters(fields, query_params)
