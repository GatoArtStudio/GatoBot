from typing import Callable, List, Dict

from core.enums.e_event_type import EventType
from helpers.class_singleton import class_singleton


@class_singleton
class Event:

    _listeners: Dict[EventType, List[Callable]] = {}

    def listener(self, event_type: EventType, function: Callable):
        """
        Añade un escuchador a un evento
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []

        self._listeners[event_type].append(function)

    def emit(self, event_type: EventType, *args, **kwargs):
        """
        Emite un evento
        """
        if event_type in self._listeners:
            for function in self._listeners[event_type]:
                function(*args, **kwargs)