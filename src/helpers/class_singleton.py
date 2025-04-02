import threading


def class_singleton(cls):
    """
        Decorador para aplicar el patrón Singleton a una clase.
        Garantiza que solo haya una instancia de la clase.
        ```python
        @class_singleton
        class MyClass:
            pass
        ```
    """
    instances = dict()
    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper