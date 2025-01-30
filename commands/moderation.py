import discord
import datetime
import typing
import logging
from discord.ext import commands
from discord import app_commands
from log.logging_config import setup_logging

# Instancia el debug
setup_logging()
logger = logging.getLogger(__name__)

class Moderation(commands.Cog):
    '''
    Comandos de moderación
    '''
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    


    
    @app_commands.command(name='purge', description='Elimina los mensajes de un usuario en las ultimas horas.')
    @commands.has_permissions(administrator=True)
    async def purge_user(self, interaction: discord.Interaction, user: discord.Member, horas: typing.Literal[7, 24, 48, 72] = 24) -> None:
        """Elimina los mensajes de un usuario en las ultimas horas.

        Args:
            interaction (discord.Interaction): La interaccion que se realiz  este comando.
            user (discord.Member): El usuario cuyos mensajes se van a eliminar.
            horas (int, optional): El numero de horas que se considerar  n recientes. Defaults to 24.

        Returns:
            None
        """
        # Compruba si el usuario tiene permisos de administracion
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return
        
        now = datetime.datetime.now(datetime.timezone.utc)
        time_limit = now - datetime.timedelta(hours=horas)

        def is_recent_and_from_user(message: discord.Message) -> bool:
            """Verifica si un mensaje es reciente y lo hizo el usuario especificado.

            Args:
                message (discord.Message): El mensaje a verificar.

            Returns:
                bool: True si es reciente y lo hizo el usuario especificado, False en caso contrario.
            """
            return message.author == user and message.created_at >= time_limit

        deleted_messages = await interaction.channel.purge(limit=1000, check=is_recent_and_from_user)
        await interaction.response.send_message(
            f'Se han eliminado {len(deleted_messages)} mensajes de {user.display_name} de las ultimas {horas} horas.',
            ephemeral=True
        )
    
    @app_commands.command(name='timeout', description='Aisla por x numero de minutos')
    @commands.has_permissions(ban_members=True)
    async def timeout_user(self, interaction: discord.Interaction, user: discord.Member, minutos: int = 5):
        # Compruba si el usuario tiene permisos de administracion
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return
        try:
            # Aisla al usuario
            timeout_expiry = datetime.timedelta(minutes=minutos)
            await user.timeout(timeout_expiry, reason=f"Aislado por {minutos} minutos, por el usuario {interaction.user.display_name}")
            # Response del comando
            await interaction.response.send_message(f'{user.mention} ha sido aislado por {minutos} minutos', ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("No tengo permisos para aislar a este usuario.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Ocurrió un error al intentar aislar al usuario: {user.mention}, error: {e}", ephemeral=True)

    @app_commands.command(name='untimeout', description='Desaisla a un usuario')
    @commands.has_permissions(ban_members=True)
    async def untimeout_user(self, interaction: discord.Interaction, user: discord.Member):
        # Compruba si el usuario tiene permisos de administracion
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return
        try:
            # Desaisla al usuario
            await user.timeout(None)
            # Response del comando
            await interaction.response.send_message(f'{user.mention} ha sido desaislad@', ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("No tengo permisos para desaislar a este usuario.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Ocurrió un error al intentar desaislar al usuario: {user.mention}, error: {e}", ephemeral=True)
    
    @app_commands.command(name='ban', description='Banea a un usuario')
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, interaction: discord.Interaction, user: discord.Member, motivo: typing.Optional[str] = None, delete_message_days: typing.Optional[int] = 1):
        # Compruba si el usuario tiene permisos de administracion
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return
        try:
            # Banea al usuario
            if motivo is None:
                motivo = "No especificado"

            await user.ban(reason=motivo, delete_message_days=delete_message_days)
            # Response del comando
            await interaction.response.send_message(f'{user.mention} ha sido baneado', ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("No tengo permisos para banear a este usuario.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Ocurrio un error al intentar banear al usuario: {user.mention}, error: {e}", ephemeral=True)
    
    @app_commands.command(name='unban', description='Desbanea a un usuario')
    @commands.has_permissions(ban_members=True)
    async def unban_user(self, interaction: discord.Interaction, user: discord.User, motivo: typing.Optional[str] = None):
        # Compruba si el usuario tiene permisos de administracion
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return
        try:
            # Desbanea al usuario
            if motivo is None:
                motivo = "No especificado"

            await interaction.guild.unban(user, reason=motivo)
            # Response del comando
            await interaction.response.send_message(f'{user.mention} ha sido desbaneado', ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("No tengo permisos para desbanear a este usuario.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Ocurrio un error al intentar desbanear al usuario: {user.mention}, error: {e}", ephemeral=True)
    
    @app_commands.command(name='kick', description='Expulsa a un usuario')
    @app_commands.describe(user="Usuario a expulsar", motivo="Motivo de la expulsión")
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, interaction: discord.Interaction, user: discord.Member, motivo: typing.Optional[str] = None):
        # Compruba si el usuario tiene permisos de administracion
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return
        try:
            # Expulsa al usuario
            if motivo is None:
                motivo = "No especificado"

            await user.kick(reason=motivo)
            # Response del comando
            await interaction.response.send_message(f'{user.mention} ha sido expulsado', ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("No tengo permisos para expulsar a este usuario.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Ocurrio un error al intentar expulsar al usuario: {user.mention}, error: {e}", ephemeral=True)




async def setup(bot):
    '''
    Agrega el cog al bot
    '''
    await bot.add_cog(Moderation(bot))