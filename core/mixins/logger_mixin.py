import logging


class LoggerMixin(object):
    """
    Миксин для получения логгеров по классам
    """

    @property
    def logger(self):
        name = '.'.join([self.__class__.__name__])
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(name)
