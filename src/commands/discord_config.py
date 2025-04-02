import discord
import typing
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions
from sqlalchemy.orm import Session

from database.connection import Database
from models.guild_discord import GuildDiscord


class DiscordConfig(commands.Cog):
    """Comandos para configurar el bot en tu servidor de Discord."""

    session_database: Session

    def __init__(self, bot):
        self.bot = bot
        self.session_database = Database().get_session()

    dc = app_commands.Group(name='discord', description='Comandos para configurar el bot en tu servidor de Discord.')

    @dc.command(name="set_log_channel", description='Configura el canal de logs, donde se enviará la actividad y acciones del bot.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def set_log_channel(self, interaction: discord.Interaction, channel: typing.Optional[discord.TextChannel] = None):
        """Configura el canal de logs"""

        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild.id
        log_channel_id = interaction.channel.id if channel is None else channel.id

        # Utilizamos la sesión de la base de datos para actualizar la tabla guild_discord
        guild = self.session_database.query(GuildDiscord).filter_by(guild_id = guild_id).first()
        if guild is None:
            guild = GuildDiscord(guild_id = guild_id, log_channel_id = log_channel_id)
            self.session_database.add(guild)
        else:
            guild.log_channel_id = log_channel_id

        self.session_database.commit()

        await interaction.followup.send(f'El canal {channel.mention} fue configurado como el canal de logs.', ephemeral=True)

    @dc.command(name='set_warning_channel', description='Configura el canal de advertencias, enviara notificaciones a los sancionados.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def set_warning_channel(self, interaction: discord.Interaction, channel: typing.Optional[discord.TextChannel] = None):
        """
        Configura canal de warnings
        """
        
        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild.id
        warning_channel_id = interaction.channel.id if channel is None else channel.id

        # Utilizamos la sesión de la base de datos para actualizar la tabla guild_discord
        guild = self.session_database.query(GuildDiscord).filter_by(guild_id = guild_id).first()
        if guild is None:
            guild = GuildDiscord(guild_id = guild_id, warning_channel_id = warning_channel_id)
            self.session_database.add(guild)
        else:
            guild.warning_channel_id = warning_channel_id

        self.session_database.commit()

        await interaction.followup.send(f'El canal {channel.mention} fue configurado como el canal de warnings.', ephemeral=True)

    @dc.command(name='set_announcement_channel', description='Configura el canal de anuncios, donde puedes anunciar actualizaciones o demas.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def set_announcement_channel(self, interaction: discord.Interaction, channel: typing.Optional[discord.TextChannel] = None):
        """
        Configura canal de announcements
        """
        
        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild.id
        announcement_channel_id = interaction.channel.id if channel is None else channel.id

        guild = self.session_database.query(GuildDiscord).filter_by(guild_id = guild_id).first()
        if guild is None:
            guild = GuildDiscord(guild_id = guild_id, announcement_channel_id = announcement_channel_id)
            self.session_database.add(guild)
        else:
            guild.announcement_channel_id = announcement_channel_id

        self.session_database.commit()

        await interaction.followup.send(f'El canal {channel.mention} fue configurado como el canal de announcements.', ephemeral=True)

    @dc.command(name='set_sanction_channel', description='Configura el canal de sanciones, donde notifica a los usuarios sobre sanciones.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def set_asanction_channel(self, interaction: discord.Interaction, channel: typing.Optional[discord.TextChannel] = None):
        """
        Configura canal de sanction
        """
        
        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild.id
        sanction_channel_id = interaction.channel.id if channel is None else channel.id

        guild = self.session_database.query(GuildDiscord).filter_by(guild_id = guild_id).first()
        if guild is None:
            guild = GuildDiscord(guild_id = guild_id, sanction_channel_id = sanction_channel_id)
            self.session_database.add(guild)
        else:
            guild.sanction_channel_id = sanction_channel_id

        self.session_database.commit()

        await interaction.followup.send(f'El canal {channel.mention} fue configurado como el canal de sanctions.', ephemeral=True)
    
    @dc.command(name='send_log', description='Envia un mensaje al canal de logs.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def send_log(self, interaction: discord.Interaction, message: str):
        
        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild.id

        guild = self.session_database.query(GuildDiscord).filter_by(guild_id = guild_id).first()
        if guild is None:
            await interaction.followup.send('No se ha configurado un canal de logs.', ephemeral=True)
            return

        if guild.log_channel_id is None:
            await interaction.followup.send('No se ha configurado un canal de logs.', ephemeral=True)
            return

        channel = interaction.guild.get_channel(guild.log_channel_id)
        if channel is None:
            await interaction.followup.send('No se ha configurado un canal de logs.', ephemeral=True)
            return

        await channel.send(message)
        await interaction.followup.send('El mensaje ha sido enviado al canal de logs.', ephemeral=True)

    @dc.command(name='set_antispam', description='Configura si el antispam esta activado o no.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def set_antispam(self, interaction: discord.Interaction, enable: bool):
        """
        Configura el antispam
        """

        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild.id

        guild = self.session_database.query(GuildDiscord).filter_by(guild_id = guild_id).first()
        if guild is None:
            guild = GuildDiscord(guild_id = guild_id, active_antispam = enable)
            self.session_database.add(guild)
        else:
            guild.active_antispam = enable

        self.session_database.commit()

        await interaction.followup.send(f'El antispam ha sido configurado como {enable}.', ephemeral=True)

    @dc.command(name='get_config', description='Obtiene la configuracion del servidor.')
    @has_permissions(administrator=True) # Verifica que el usuario tenga permisos de administrador
    async def get_config(self, interaction: discord.Interaction):
        """
        Obtiene la configuracion del servidor
        """

        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild.id

        guild = self.session_database.query(GuildDiscord).filter_by(guild_id = guild_id).first()
        if guild is None:
            await interaction.followup.send('No se ha configurado un canal de logs.', ephemeral=True)
            return

        embed = discord.Embed(title="Configuración del servidor", color=discord.Color.green())
        embed.add_field(name="Canal de logs", value=f"<#{guild.log_channel_id}>" if guild.log_channel_id is not None else "No configurado", inline=False)
        embed.add_field(name="Canal de announcements", value=f"<#{guild.announcement_channel_id}>" if guild.announcement_channel_id is not None else "No configurado", inline=False)
        embed.add_field(name="Canal de sanctions", value=f"<#{guild.sanction_channel_id}>" if guild.sanction_channel_id is not None else "No configurado", inline=False)
        embed.add_field(name='Canal de Warning', value=f"<#{guild.warning_channel_id}>" if guild.warning_channel_id is not None else "No configurado", inline=False)
        embed.add_field(name="Activar antispam", value=f"{guild.active_antispam}", inline=False)

        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(DiscordConfig(bot))
