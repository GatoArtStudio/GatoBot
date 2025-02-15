import discord
import typing
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions, bot_has_permissions
from base.guild_discord import GuildDiscord

class DiscordConfig(commands.Cog):
    """Comandos para configurar el bot en tu servidor de Discord."""
    def __init__(self, bot):
        self.bot = bot

    dc = app_commands.Group(name='discord', description='Comandos para configurar el bot en tu servidor de Discord.')

    @dc.command(name="set_log_channel", description='Configura el canal de logs, donde se enviará la actividad y acciones del bot.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def set_log_channel(self, interaction: discord.Interaction, channel: typing.Optional[discord.TextChannel] = None):
        """Configura el canal de logs"""

        await interaction.response.defer(ephemeral=True)

        db = GuildDiscord(interaction.guild.id)

        if channel is None:
            result = db.set_log_channel(interaction.channel.id)
            if result:
                await interaction.followup.send(f'El canal {interaction.channel.mention} fue configurado como el canal de logs.', ephemeral=True)
            else:
                await interaction.followup.send(f'El canal {interaction.channel.mention} no pudo ser configurado como el canal de logs.', ephemeral=True)
        else:
            result = db.set_log_channel(channel.id)
            if result:
                await interaction.followup.send(f'El canal {channel.mention} fue configurado como el canal de logs.', ephemeral=True)
            else:
                await interaction.followup.send(f'El canal {channel.mention} no pudo ser configurado como el canal de logs.', ephemeral=True)
    
    @dc.command(name='set_warning_channel', description='Configura el canal de advertencias, enviara notificaciones a los sancionados.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def set_warning_channel(self, interaction: discord.Interaction, channel: typing.Optional[discord.TextChannel] = None):
        """
        Configura canal de warnings
        """
        
        await interaction.response.defer(ephemeral=True)

        db = GuildDiscord(interaction.guild.id)

        if channel is None:
            result = db.set_warning_channel(interaction.channel.id)
            if result:
                await interaction.followup.send(f'El canal {interaction.channel.mention} fue configurado como el canal de warnings.', ephemeral=True)
            else:
                await interaction.followup.send(f'El canal {interaction.channel.mention} no pudo ser configurado como el canal de warnings.', ephemeral=True)
        else:
            result = db.set_warning_channel(channel.id)
            if result:
                await interaction.followup.send(f'El canal {channel.mention} fue configurado como el canal de warnings.', ephemeral=True)
            else:
                await interaction.followup.send(f'El canal {channel.mention} no pudo ser configurado como el canal de warnings.', ephemeral=True)
    
    @dc.command(name='set_announcement_channel', description='Configura el canal de anuncios, donde puedes anunciar actualizaciones o demas.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def set_announcement_channel(self, interaction: discord.Interaction, channel: typing.Optional[discord.TextChannel] = None):
        """
        Configura canal de announcements
        """
        
        await interaction.response.defer(ephemeral=True)

        db = GuildDiscord(interaction.guild.id)

        if channel is None:
            result = db.set_announcement_channel(interaction.channel.id)
            if result:
                await interaction.followup.send(f'El canal {interaction.channel.mention} fue configurado como el canal de announcements.', ephemeral=True)
            else:
                await interaction.followup.send(f'El canal {interaction.channel.mention} no pudo ser configurado como el canal de announcements.', ephemeral=True)
        else:
            result = db.set_announcement_channel(channel.id)
            if result:
                await interaction.followup.send(f'El canal {channel.mention} fue configurado como el canal de announcements.', ephemeral=True)
            else:
                await interaction.followup.send(f'El canal {channel.mention} no pudo ser configurado como el canal de announcements.', ephemeral=True)

    @dc.command(name='set_sanction_channel', description='Configura el canal de sanciones, donde notifica a los usuarios sobre sanciones.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def set_asanction_channel(self, interaction: discord.Interaction, channel: typing.Optional[discord.TextChannel] = None):
        """
        Configura canal de sanction
        """
        
        await interaction.response.defer(ephemeral=True)

        db = GuildDiscord(interaction.guild.id)

        if channel is None:
            result = db.set_sanction_channel(interaction.channel.id)
            if result:
                await interaction.followup.send(f'El canal {interaction.channel.mention} fue configurado como el canal de sanctions.', ephemeral=True)
            else:
                await interaction.followup.send(f'El canal {interaction.channel.mention} no pudo ser configurado como el canal de sanctions.', ephemeral=True)
        else:
            result = db.set_sanction_channel(channel.id)
            if result:
                await interaction.followup.send(f'El canal {channel.mention} fue configurado como el canal de sanctions.', ephemeral=True)
            else:
                await interaction.followup.send(f'El canal {channel.mention} no pudo ser configurado como el canal de sanctions.', ephemeral=True)
    
    @dc.command(name='send_log', description='Envia un mensaje al canal de logs.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def send_log(self, interaction: discord.Interaction, message: str):
        
        await interaction.response.defer(ephemeral=True)

        db = GuildDiscord(interaction.guild.id)

        channel = db.get_log_channel()
        if channel is None:
            await interaction.followup.send('No se ha configurado un canal de logs.', ephemeral=True)
            return
        
        channel = interaction.guild.get_channel(channel)
        if channel is None:
            await interaction.followup.send('No se ha configurado un canal de logs.', ephemeral=True)
            return

        await channel.send(message)

async def setup(bot):
    await bot.add_cog(DiscordConfig(bot))
