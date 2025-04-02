from abc import ABC, abstractmethod

class IInfrastructureInitiator(ABC):

    def start_service(self):
        """
        Inicia la infraestructura
        """
        self.on_load()
        self.on_enable()

    def stop_service(self):
        """
        Detiene la infraestructura
        """
        self.on_disable()

    @abstractmethod
    def on_load(self) -> None:
        """
        Called when the infrastructure is loaded.
        This method should handle any necessary initialization operations
        such as loading configuration data or setting up the infrastructure state.
        """
        pass

    @abstractmethod
    def on_enable(self) -> None:
        """
        Called when the infrastructure is enabled or started.
        This method should handle any necessary initialization operations
        such as starting processes or allocating resources.
        """
        pass

    @abstractmethod
    def on_disable(self) -> None:
        """
        Called when the infrastructure is disabled or stopped.
        This method should handle any necessary cleanup operations
        such as releasing resources or stopping ongoing processes.
        """
        pass