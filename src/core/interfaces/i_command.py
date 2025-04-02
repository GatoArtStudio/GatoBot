from abc import ABC, abstractmethod

class ICommand(ABC):
    """
    Interfaz para los comandos
    """
    @abstractmethod
    def execute(self):
        """
        Se llama cuando se ejecuta el comando
        """
        pass