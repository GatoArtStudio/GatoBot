from abc import ABC, abstractmethod

class IDiscordBot(ABC):

    @abstractmethod
    def run(self) -> None:
        """
        Se llama para iniciar el bot
        """
        pass

    @abstractmethod
    async def on_ready(self) -> None:
        """
        Se llama cuando el bot esta listo o iniciado completamente
        """
        pass

    @abstractmethod
    async def setup_hook(self) -> None:
        """
        Se llama para configurar los manejadores de eventos u otras funcionalidades
        """
        pass

    @abstractmethod
    def run_bot(self) -> None:
        """
        Se llama para iniciar el bot
        """
        pass

    @abstractmethod
    def stop_bot(self) -> None:
        """
        Se llama para detener el bot
        """
        pass

