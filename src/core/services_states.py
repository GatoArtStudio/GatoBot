from helpers.class_singleton import class_singleton

@class_singleton
class ServicesStates:
    """
    Clase para manejar el estado de la app
    """
    _data: dict

    def __init__(self):
        self._data = {}

    def set(self, key, value):
        """
        Setea un dato
        :param key:
        :param value:
        :return:
        """
        self._data[key] = value

    def get(self, key, default = None):
        """
        Obtiene un dato
        :param key:
        :param default:
        :return:
        """
        return self._data.get(key, default)