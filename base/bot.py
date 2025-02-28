import discord
from discord.ext import commands
import os
import datetime
from config import TOKEN
from log import Logger
import view.ui_dc as ui
from utils import music_utils

# Configuración de logging
logger = Logger().get_logger()

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start_time = None
        self._is_ready = False

    @property
    def uptime(self):
        if self._start_time is None:
            return None
        return datetime.datetime.utcnow() - self._start_time

    @property
    def is_ready(self):
        return self._is_ready

    async def setup_hook(self):
        self.add_view(ui.MenuMusica())
        await self.load_extensions()

    async def load_extensions(self):
        # Cargar extensiones de eventos
        for filename in os.listdir('./event'):
            if filename.endswith('.py'):
                await self.load_extension(f'event.{filename[:-3]}')
        
        # Cargar extensiones de comandos
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                await self.load_extension(f'commands.{filename[:-3]}')

    async def on_ready(self):
        self._start_time = datetime.datetime.utcnow()
        self._is_ready = True
        logger.info(f'Conectado como {self.user.name} ({self.user.id})')
        music_utils.bot = self

        try:
            logger.info('Sincronizando comandos...')
            synced = await self.tree.sync()
            logger.info(f'Sincronizado {len(synced)} comando(s)')
        except Exception as e:
            logger.error(f'Error sincronizando comandos: {e}')

    async def on_disconnect(self):
        self._is_ready = False
        logger.warning("Bot desconectado")

bot = Bot(command_prefix='/', intents=discord.Intents.all())