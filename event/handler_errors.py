import discord
import time
from discord.ext import commands
from discord import app_commands
from log.logging_config import Logger
from service.guild_manager_discord import GuildManagerDiscord

# Instancia el debug
logger = Logger().get_logger()

class HandlerErrorCommands(commands.Cog):
    '''
    Comandos de moderación
    '''
    async def on_app_command_error(interaction: discord.Interaction, error, bot: commands.Bot):

        await interaction.response.defer(ephemeral=True)

        if isinstance(error, app_commands.MissingPermissions):

            embed = discord.Embed(title="No tienes permisos", description="No tienes permisos para usar este comando.", color=discord.Color.red())
            await interaction.followup.send(embed=embed, ephemeral=True)

            guild_manager = GuildManagerDiscord(interaction.guild.id, bot)
            await guild_manager.send_log_commands_missing_permissions(interaction, error)
            
            return
        
        embed = discord.Embed(title="Error", description="Ocurrio un error al ejecutar el comando.", color=discord.Color.red())
        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    '''
    Agrega el cog al bot
    '''
    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error):
        await HandlerErrorCommands.on_app_command_error(interaction, error, bot)