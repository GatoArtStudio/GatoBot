import discord
import logging
import typing
import threading
from discord.ext import commands
from discord import app_commands
from log.logging_config import setup_logging
from service.server_proxy import ServerProxy
from config import USER_DEV_ID
from utils import ColorDiscord

setup_logging()
logger = logging.getLogger(__name__)


class ExternalUtils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='update_announcement', description='Informa en todos los canales que esta, sobre la actualizacion del bot')
    async def update_announcement(self, interaction: discord.Interaction, message: str, title: typing.Optional[str] = 'Actualización'):
        """Anuncia una actualización en todos los servidores donde está el bot.

        Args:
            interaction (discord.Interaction): La interacción que invocó este comando.
            message (str): El mensaje de actualización a anunciar.
        """
        if interaction.user.id == int(USER_DEV_ID):
            interaction.response.defer(ephemeral=True)
            for guild in self.bot.guilds:
                system_channel = guild.system_channel
                if system_channel is not None:
                    try:
                        message_formtated = message.replace('\\n', '\n')
                        embed = discord.Embed(
                            title=title,
                            description=message_formtated,
                            color=ColorDiscord.AQUA.value
                        )
                        await system_channel.send(embed=embed)
                    except discord.errors.Forbidden:
                        logger.warning(f'No tengo permiso para enviar el mensaje en el canal {system_channel.mention} del servidor {guild.name}')
                        await interaction.response.send_message(f'No tengo permiso para enviar el mensaje en el canal {system_channel.mention} del servidor {guild.name}', ephemeral=True)
                    except discord.errors.HTTPException:
                        logger.warning(f'No puedo enviar el mensaje en el canal {system_channel.mention} del servidor {guild.name}')
                        await interaction.response.send_message(f'No puedo enviar el mensaje en el canal {system_channel.mention} del servidor {guild.name}', ephemeral=True)
        else:
            await interaction.response.send_message("No tienes permisos para usar este comando, solo el desarrollador.", ephemeral=True)

async def setup(bot):
    '''
    Agrega el cog al bot
    '''
    await bot.add_cog(ExternalUtils(bot))