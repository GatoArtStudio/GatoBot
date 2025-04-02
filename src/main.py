import logging
import discord
from typing import List

from database.connection import Database
from services.cloudflared_tunnel import CloudflaredTunnel
from core.implements.discord_bot import DiscordBot
from services.servidor_web import ServidorWeb
from core.invokers.service_invoker import ServiceInvoker
from core.commands.service_command import ServiceCommand
from core.interfaces.i_infrastructure_initiator import IInfrastructureInitiator
from core.logging import Logger

class Main(IInfrastructureInitiator):

    _discord_bots: List[DiscordBot] = []
    _service_invoker: ServiceInvoker
    _services_receivers: List[ServiceCommand] = []
    _logger: logging.Logger

    def __init__(self):
        self._logger = Logger('deployment_system').get_logger()
        self.start_service()

    def on_load(self) -> None:
        """
        Instancia y preconfigura todos los servicios
        """
        self._logger.info("Cargando servicios")

        self._service_invoker = ServiceInvoker()

        database = Database()
        database.create_tables()

        # Agregamos los objetos que van a recibir instrucciones de el comando ServiceCommand
        self._services_receivers.append(
            ServiceCommand(
                DiscordBot(command_prefix='/', intents=discord.Intents.all())
            )
        )
        self._services_receivers.append(
            ServiceCommand(
                CloudflaredTunnel()
            )
        )
        self._services_receivers.append(
            ServiceCommand(
                ServidorWeb()
            )
        )

    def on_enable(self) -> None:
        """
        Habilita todos los servicios preconfigurados y cargados
        """
        self._logger.info("Habilitando servicios")

        # Enviar señal de inicio a los servicios
        if self._services_receivers:
            self._service_invoker.send_signal_start(self._services_receivers)

        # Esperamos a que halla una interrupcion para detener los servicios
        try:
            self._logger.warning("Esperando interrupcion para detener los servicios")
            while True:
                pass
        except KeyboardInterrupt:
            self._logger.info("Deteniendo servicios")
        finally:
            self.on_disable()

    def on_disable(self) -> None:
        """
        Se ejecuta cuando la infraestructura se deshabilita
        """
        self._logger.info("Deshabilitando servicios")

        # Enviar señal de parada a los servicios
        if self._services_receivers:
            self._service_invoker.send_signal_stop()


if __name__ == "__main__":
    main = Main()