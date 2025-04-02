import asyncio
import logging
import threading
from abc import abstractmethod

from core.interfaces.i_infrastructure_initiator import IInfrastructureInitiator


class ServiceThread(IInfrastructureInitiator):

    logger: logging.Logger
    _process: any
    _shutdown_event: asyncio.Event
    _thread: threading.Thread

    def on_disable(self) -> None:
        """
        Called when the service is disabled or stopped.
        This method should handle any necessary cleanup operations
        such as releasing resources or stopping ongoing processes.
        """
        self._shutdown_event.set()

    def on_enable(self) -> None:
        """
        Called when the service is enabled or started.
        This method should handle any necessary initialization operations
        such as starting processes or allocating resources.
        """
        def run_service():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(
                asyncio.gather(
                    self.run_service(),
                    return_exceptions=True
                )
            )
            loop.close()

        try:
            self._thread = threading.Thread(
                target=run_service,
                daemon=True
            )
            self._thread.start()
        except Exception as e:
            self.logger.error(f"Error al iniciar el servicio: {str(e)}")


    def on_load(self) -> None:
        """
        Called when the service is loaded.
        This method should handle any necessary initialization operations
        such as loading configuration data or setting up the service state.
        """
        self._shutdown_event = asyncio.Event()

    @abstractmethod
    async def run_service(self) -> None:
        """
        Logic to start the service
        """
        pass