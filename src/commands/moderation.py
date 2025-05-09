import logging
import re
import discord
import datetime
import typing
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions

from core.implements.discord_bot import DiscordBot
from core.logging import Logger

# Instancia el debug
logger: logging.Logger

class Moderation(commands.Cog):
    """
    Comandos de moderación
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name='purge', description='Elimina los mensajes de un usuario en las ultimas horas.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def purge_user(self, interaction: discord.Interaction, user: discord.Member, horas: typing.Literal[7, 24, 48, 72] = 24) -> None:
        """Elimina los mensajes de un usuario en las ultimas horas.

        Args:
            interaction (discord.Interaction): La interaccion que se realiz  este comando.
            user (discord.Member): El usuario cuyos mensajes se van a eliminar.
            horas (int, optional): El numero de horas que se considerar  n recientes. Defaults to 24.

        Returns:
            None
        """

        
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
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def timeout_user(self, interaction: discord.Interaction, user: discord.Member, minutos: int = 5):

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
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def untimeout_user(self, interaction: discord.Interaction, user: discord.Member):

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
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def ban_user(self, interaction: discord.Interaction, user: discord.Member, motivo: typing.Optional[str] = None, delete_message_days: typing.Optional[int] = 1):

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
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def unban_user(self, interaction: discord.Interaction, user: discord.User, motivo: typing.Optional[str] = None):

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
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def kick_user(self, interaction: discord.Interaction, user: discord.Member, motivo: typing.Optional[str] = None):

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

    @app_commands.command(name='setup_security', description='Configura el servidor con unas configuraciones pre-configuradas, mas informacion en la web del bot.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    @app_commands.describe(hidden = 'Oculta el mensaje de respuesta.', ignored_roles = 'Lista de roles a ignorar, debes mencionar los roles a ignorar usando el @.')
    async def setup_security(self, interaction: discord.Interaction, hidden: bool = False, ignored_roles: typing.Optional[str] = None):
        """Configura el servidor con unas configuraciones pre-configuradas.

        Args:
            interaction (discord.Interaction): La interaccion que se realiza este comando.
            hidden (bool, optional): Indica si el mensaje de respuesta debe ser oculto. Defaults to False.
            ignored_roles (List[discord.Role], optional): Lista de roles a ignorar. Defaults to None.
        """
        # Si hay roles ignorados, convertirlos a objetos discord.Role
        roles = []
        if ignored_roles:
            for role_id in re.findall(r'\d{17,19}', ignored_roles):
                role = interaction.guild.get_role(int(role_id))
                if role:
                    roles.append(role)

        await interaction.response.defer(ephemeral=hidden)

        guild = interaction.guild
        roles_modified = []
        count = 0
        ignored_roles_ids = [role.id for role in roles] if roles else []

        for role in guild.roles:
            # Ignorar los roles especificados
            if role.id in ignored_roles_ids:
                continue

            # Modificar los permisos de los roles
            if not role.permissions.administrator:
                try:
                    new_perms = role.permissions
                    new_perms.update(
                        use_external_apps=False,
                        manage_webhooks=False,
                        mention_everyone=False
                    )

                    await role.edit(permissions=new_perms)
                    roles_modified.append(role.mention)
                    count += 1

                except Exception as e:
                    logger.error(f"Error al intentar modificar los permisos del rol {role.name}: {e}")
                    continue
        
        embed = discord.Embed(
            title="Configuración de seguridad",
            description=f"Se han modificado los permisos de {count} roles en el servidor.",
            color=discord.Color.green()
        )

        # Dividir la lista de roles modificados en múltiples campos si es necesario
        roles_modified_str = ", ".join(roles_modified)
        max_length = 1000
        for i in range(0, len(roles_modified_str), max_length):
            embed.add_field(name="Roles modificados", value=roles_modified_str[i:i+max_length], inline=False)
            
        embed.add_field(name="Permisos modificados", value="`use_external_apps`, `manage_webhooks`, `mention_everyone`", inline=False)

        await interaction.followup.send(embed=embed)


async def setup(bot: DiscordBot):
    """
    Agrega el cog al bot
    """

    global logger
    logger = bot.logger

    await bot.add_cog(Moderation(bot))