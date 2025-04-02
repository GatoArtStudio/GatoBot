import time
import typing
import discord
from functools import wraps

class HandlerLogsTools:
    def create_embed_channeltext_logs(self, title: str, color: discord.Color, creator: int, text_channel: discord.TextChannel):

        embed = discord.Embed(title=title, color=color)
        embed.add_field(name="Canal", value=f"{text_channel.name}", inline=True)
        embed.add_field(name="ID", value=f"{text_channel.id}", inline=True)
        embed.add_field(name="Tipo", value=f"{text_channel.type}", inline=True)
        embed.add_field(name="Categoria", value=f"{text_channel.category}", inline=True)
        embed.add_field(name="Categoria ID", value=f"{text_channel.category.id}", inline=True)
        embed.add_field(name="Autor", value=f"<@{creator}>", inline=True)
        embed.add_field(name="Tiempo", value=f"<t:{int(time.time())}:R>", inline=True)
        embed.add_field(name="Posicion", value=f"{text_channel.position}", inline=False)
        embed.add_field(name="NSFW", value=f"{text_channel.nsfw}", inline=False)
        embed.add_field(name="Tema", value=f"{text_channel.topic}", inline=True)
        embed.add_field(name="Mencion", value=f"{text_channel.mention}", inline=True)

        return embed
    
    async def get_author_channel_changes_id(self, guild: discord.Guild, channel_id: int, action: typing.Union[discord.AuditLogAction.channel_create, discord.AuditLogAction.channel_delete, discord.AuditLogAction.channel_update]):
        """
        Obtiene el ID del usuario que realizó un cambio en el canal.

        Args:
            guild (discord.Guild): El servidor donde ocurrió el cambio.
            channel_id (int): El ID del canal que fue cambiado.
            action (Union[discord.AuditLogAction]): La acción de auditoría a buscar (crear, eliminar, actualizar).

        Returns:
            Optional[int]: El ID del usuario que realizó el cambio, o None si no se encuentra.
        """

        if action not in [discord.AuditLogAction.channel_create, discord.AuditLogAction.channel_delete, discord.AuditLogAction.channel_update]:
            raise ValueError('Error: action must be a discord.AuditLogAction.channel_create or discord.AuditLogAction.channel_delete or discord.AuditLogAction.channel_update')
    
        async for entry in guild.audit_logs(limit=1, action=action):
            if entry.target.id == channel_id:
                return entry.user.id
            
        return None
    
    async def get_author_invite_id(self, guild: discord.Guild, invite_id: int, action: typing.Union[discord.AuditLogAction.invite_create, discord.AuditLogAction.invite_delete]):
        """
        Obtiene el ID del usuario que realizó un cambio en el canal.

        Args:
            guild (discord.Guild): El servidor donde ocurrió el cambio.
            channel_id (int): El ID del canal que fue cambiado.
            action (Union[discord.AuditLogAction]): Laacción de auditoría a buscar (crear, eliminar, actualizar).

        Returns:
            Optional[int]: El ID del usuario que realizó el cambio, o None si no se encuentra.
        """

        if action not in [discord.AuditLogAction.invite_create, discord.AuditLogAction.invite_delete]:
            raise ValueError('Error: action must be a discord.AuditLogAction.invite_create or discord.AuditLogAction.invite_delete')
    
        async for entry in guild.audit_logs(limit=1, action=action):
            if entry.target.id == invite_id:
                return entry.user.id
            
        return None
    
    @staticmethod
    def ensure_log_channel(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            log_channel_id = self.db.get_log_channel()
            if log_channel_id != 0 and log_channel_id is not None:
                interaction = kwargs.get('interaction') or args[0]
                log_channel = interaction.guild.get_channel(log_channel_id)
                if log_channel is not None:
                    return await func(self, log_channel, *args, **kwargs)
            # Opcional: manejar el caso en que no se encuentra el canal de registro
            print("Log channel not found or not configured.")
        return wrapper