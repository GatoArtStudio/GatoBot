import logging

import discord
import threading
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions
from sqlalchemy.orm import Session

from core.implements.discord_bot import DiscordBot
from services.server_proxy import ServerProxy
from database.connection import Database

# Instancia el debug
logger: logging.Logger

class ServerProxyCommands(commands.Cog):

    session_database: Session

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ps = None
        self.servidor_proxy_thread = None
        self.session_database = Database().get_session()

    @app_commands.command(name='ip_add_proxy', description='Agrega una ip al servidor proxy')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async  def ip_add_proxy(self, interaction: discord.Interaction, ip: str):

        if self.ps is None:
            await interaction.response.send_message("El servidor proxy no esta iniciado.", ephemeral=True)
            return
        self.ps.add_ip_whitelist(ip)
        await interaction.response.send_message(f'IP {ip} agregada al servidor proxy', ephemeral=True)

    @app_commands.command(name='ip_del_proxy', description='Elimina una ip del servidor proxy')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async  def ip_del_proxy(self, interaction: discord.Interaction, ip: str):

        if self.ps is None:
            await interaction.response.send_message("El servidor proxy no esta iniciado.", ephemeral=True)
            return
        self.ps.remove_ip_whitelist(ip)
        await interaction.response.send_message(f'IP {ip} eliminada del servidor proxy', ephemeral=True)

    @app_commands.command(name='ip_list_proxy', description='Muestra las ips del servidor proxy')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async  def ip_list_proxy(self, interaction: discord.Interaction):

        if self.ps is None:
            await interaction.response.send_message("El servidor proxy no esta iniciado.", ephemeral=True)
            return
        await interaction.response.send_message(f'IPs del servidor proxy: {self.ps.list_ip}', ephemeral=True)

    @app_commands.command(name='ip_load_proxy', description='Carga las ips del servidor proxy')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async  def ip_load_proxy(self, interaction: discord.Interaction):

        if self.ps is None:
            await interaction.response.send_message("El servidor proxy no esta iniciado.", ephemeral=True)
            return
        self.ps.load_whitelist()
        await interaction.response.send_message(f'IPs del servidor proxy cargadas', ephemeral=True)

    @app_commands.command(name='start_server_proxy', description='inicia el servidor proxy')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async  def start_server_p(self, interaction: discord.Interaction):

        if self.ps is None or not self.ps.is_running:
            # Iniciamos el hilo del servidor proxy
            self.servidor_proxy_thread = threading.Thread(target=self.start_server_proxy, daemon=True)
            self.servidor_proxy_thread.start()
            await interaction.response.send_message(f'Servidor proxy iniciado', ephemeral=True)
        else:
            await interaction.response.send_message(f'Servidor proxy ya iniciado', ephemeral=True)

    @app_commands.command(name='stop_server_proxy', description='Detiene el servidor proxy')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async  def stop_server_P(self, interaction: discord.Interaction):

        if self.ps is not None and self.ps.is_running:
            await interaction.response.defer(ephemeral=True)
            try:
                r = self.stop_server_proxy()
                if r:
                    await interaction.followup.send(f'Servidor proxy detenido', ephemeral=True)
                    return
                else:
                    await interaction.followup.send(f'Servidor proxy no detenido', ephemeral=True)
                    return
            except Exception as e:
                logger.error(f'Error al detener el servidor proxy: {e}')
                await interaction.followup.send(f'Error al detener el servidor proxy: {e}', ephemeral=True)
                return
        else:
            await interaction.response.send_message(f'Servidor proxy no iniciado', ephemeral=True)

    # Iniciamos servidor proxy
    def start_server_proxy(self):
        '''
        Inicia el servidor proxy
        '''
        # Si el servidor esta corriendo, no debe iniciarce y se retonar false
        if self.ps is None:
            logger.info('Iniciando servidor proxy')
            self.ps = ServerProxy()
            self.ps.start_proxy()

    # Detenemos el servidor proxy
    def stop_server_proxy(self):
        '''
        Detiene el servidor proxy
        '''

        if self.ps is None:
            return False
        if self.ps.is_running:
            logger.info('Deteniendo servidor proxy')
            self.ps.stop_proxy()
            if self.servidor_proxy_thread is not None:
                self.servidor_proxy_thread.join(1.0)
            self.ps = None
            self.servidor_proxy_thread = None
            return True
        else:
            return False


async def setup(bot: DiscordBot):
    """
    Agrega el cog al bot
    """

    global logger
    logger = bot.logger

    await bot.add_cog(ServerProxyCommands(bot))