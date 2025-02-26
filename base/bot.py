import discord
from discord.ext import commands
import os
import threading
from config import TOKEN
from log import Logger
from service.server_http import ServerHTTP
from service.cloudflare_tunnel import start_cloudflare_tunnel
from utils import music_utils
import view.ui_dc as ui

# Configuración de logging
logger = Logger().get_logger()

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.servidor_http_thread = None

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
        logger.info(f'Conectado como {self.user.name} ({self.user.id})')
        music_utils.bot = self

        try:
            logger.info('Sincronizando comandos...')
            synced = await self.tree.sync()
            logger.info(f'Sincronizado {len(synced)} comando(s)')
        except Exception as e:
            logger.error(f'Tipo de error {e}')

    def start_server_http(self):
        shttp = ServerHTTP()
        shttp.start_server()

    async def start_bot(self):
        self.servidor_http_thread = threading.Thread(target=self.start_server_http, daemon=True)
        self.servidor_http_thread.start()
        start_cloudflare_tunnel()
        await self.start(TOKEN)

bot = Bot(command_prefix='/', intents=discord.Intents.all())