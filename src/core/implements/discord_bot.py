from discord import Message
from discord.ext.commands import Bot

from core.enums.e_types_services import ETypesServices
from core.interfaces.i_discord_bot import IDiscordBot
from core.interfaces.i_infrastructure_initiator import IInfrastructureInitiator
from config.config import DISCORD_TOKEN, SRC_PATH
from core.logging import Logger
from core.event import Event, EventType

from datetime import datetime, timedelta
import threading
import asyncio
import logging

from core.services_states import ServicesStates
from models.bot_discord import BotDiscord


class DiscordBot(Bot, IDiscordBot, IInfrastructureInitiator):

    _token_bot: str
    _name_bot: str = 'discord_bot'
    _thread_bot: threading.Thread
    _loop: asyncio.AbstractEventLoop
    logger: logging.Logger
    _start_time: int = None
    _is_ready: bool
    _event: asyncio.Event
    _event_manager: Event

    def __init__(self, *args, token: str = DISCORD_TOKEN, **kwargs):
        super().__init__(*args, **kwargs)
        self._token_bot = token
        self.logger = Logger(self._name_bot).get_logger()
        self._loop = None
        self._event = asyncio.Event()
        self.states = ServicesStates()
        self.states.set(ETypesServices.DISCORD_BOT.value, self)
        self._event_manager = Event()

    @property
    def uptime(self):
        if self._start_time is None:
            return None
        return datetime.utcnow() - self._start_time

    async def on_ready(self) -> None:
        self._start_time = datetime.utcnow()
        self._is_ready = True

        # Emitimos un evento de que ya esta el bot ready
        self._event_manager.emit(
            EventType.BOT_STATUS,
            BotDiscord(
                id_bot_discord=self.user.id,
                status_runtime=True,
        ))

        try:
            self.logger.info('Sincronizando comandos...')
            synced = await self.tree.sync()
            self.logger.info(f'Sincronizado {len(synced)} comando(s)')
        except Exception as e:
            self.logger.error(f'Error sincronizando comandos: {e}')
        self.logger.info(f"Bot listo como {self.user.name} ({self.user.id})")

        # Emitimos un evento de que ya esta el bot listo
        self._event_manager.emit(
            EventType.BOT_STARTED,
            self
        )

    async def setup_hook(self) -> None:
        self.logger.info(f"Configurando bot como {self._name_bot}")
        self._name_bot = self.user.name
        self.logger = Logger(self._name_bot).get_logger()

        # self.add_view(ui.MenuMusica())
        self.logger.info(f"Cargando extenciones en bot de discord...")
        await self.load_extensions()

    async def load_extensions(self) -> None:
        """
        Cargamos las extenciones para el bot
        """
        files_path_event = SRC_PATH / 'events'
        files_path_command = SRC_PATH / 'commands'

        # Cargamos los eventos
        for filename in files_path_event.glob('*.py'):
            if filename.name == '__init__.py':
                continue
            self.logger.info(f"Cargando extencion para eventos: {filename.stem}")
            await self.load_extension(f'events.{filename.stem}')

        # Cargamos los comandos
        for filename in files_path_command.glob('*.py'):
            if filename.name == '__init__.py':
                continue

            self.logger.info(f"Cargando extencion para comandos: {filename.stem}")
            await self.load_extension(f'commands.{filename.stem}')

        self.logger.info(f"Extenciones cargadas en bot de discord")

    async def on_message(self, message: Message) -> None:
        """
        Evento de mensaje
        """

        self.logger.info(f"Recibiendo mensaje de {message.author.name}: {message.content}")

    def on_load(self) -> None:
        self.logger.info(f"Cargando bot como {self._name_bot}")

    def on_enable(self) -> None:
        self.logger.info(f"Habilitando bot como {self._name_bot}")

        # Iniciar el bot
        def run_asyncio_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            self._loop.run_until_complete(asyncio.gather(self.run_bot(), return_exceptions=True))
            self._loop.close()

        # Iniciar el bot en un hilo
        self._thread_bot = threading.Thread(target=run_asyncio_loop, daemon=True)
        self._thread_bot.start()

    def on_disable(self) -> None:
        self.logger.info(f"Deshabilitando bot como {self._name_bot}")
        self._event.set()
        self._is_ready = False

        # Emitimos un evento de que ya esta el bot deshabilitado
        self._event_manager.emit(
            EventType.BOT_STATUS,
            BotDiscord(
                id_bot_discord=self.user.id,
                status_runtime=False,
            ))
        self.logger.info(f"Bot deshabilitado como {self._name_bot}")

    async def run_bot(self):
        """
        Se llama para iniciar el bot
        """
        await self.start(self._token_bot)

    def stop_bot(self) -> None:
        pass

