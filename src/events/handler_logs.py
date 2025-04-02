import logging

import discord
from discord.ext import commands

from core.implements.discord_bot import DiscordBot
from core.implements.guild_manager_discord import GuildManagerDiscord
import time

# Instancia el debug
logger: logging.Logger


class HandlerLogs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Cuando se crea o eliminan canales
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        if isinstance(channel, discord.TextChannel):
            '''
            Evento de creacion de canales
            '''

            # creamos una variable de tipo discord.TextChannel
            text_channel: discord.TextChannel = channel
            assert isinstance(text_channel, discord.TextChannel)

            guild_manager = GuildManagerDiscord(channel.guild.id, self.bot)

            creator = await guild_manager.get_author_channel_changes_id(guild=text_channel.guild, channel_id=text_channel.id, action=discord.AuditLogAction.channel_create)
            embed = guild_manager.create_embed_channeltext_logs(title='Canal Creado', color=discord.Color.green(), creator=creator, text_channel=text_channel)

            await guild_manager.send_log_raw_message(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        if isinstance(channel, discord.TextChannel):
            '''
            Evento de eliminacion de canales
            '''

            # creamos una variable de tipo discord.TextChannel
            text_channel: discord.TextChannel = channel
            assert isinstance(text_channel, discord.TextChannel)

            guild_manager = GuildManagerDiscord(channel.guild.id, self.bot)

            creator = await guild_manager.get_author_channel_changes_id(guild=text_channel.guild, channel_id=text_channel.id, action=discord.AuditLogAction.channel_delete)
            embed = guild_manager.create_embed_channeltext_logs(title='Canal Eliminado', color=discord.Color.red(), creator=creator, text_channel=text_channel)

            await guild_manager.send_log_raw_message(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        if isinstance(after, discord.TextChannel):
            '''
            Evento de actualizacion de canales
            '''

            # creamos una variable de tipo discord.TextChannel
            text_channel: discord.TextChannel = after
            assert isinstance(text_channel, discord.TextChannel)

            guild_manager = GuildManagerDiscord(after.guild.id, self.bot)

            creator = await guild_manager.get_author_channel_changes_id(guild=text_channel.guild, channel_id=text_channel.id, action=discord.AuditLogAction.channel_update)
            embed = guild_manager.create_embed_channeltext_logs(title='Canal Actualizado', color=discord.Color.orange(), creator=creator, text_channel=text_channel)

            await guild_manager.send_log_raw_message(embed=embed)
        
    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        
        guild_manager = GuildManagerDiscord(invite.guild.id, self.bot)
        await guild_manager.send_log_invite_create(invite)
    
    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        
        guild_manager = GuildManagerDiscord(invite.guild.id, self.bot)
        author_id = await guild_manager.get_author_invite_id(guild=invite.guild, invite_id=invite.id, action=discord.AuditLogAction.invite_delete)
        await guild_manager.send_log_invite_delete(invite, author_id=author_id)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        '''
        Maneja los cambios de estado de voz de un miembro.
        '''
        guild_manager = GuildManagerDiscord(member.guild.id, self.bot)

        # Unirse a un canal de voz
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(title="Unión a canal de voz", color=discord.Color.green())
            embed.add_field(name="Usuario", value=f"{member.mention}", inline=False)
            embed.add_field(name="Canal", value=f"{after.channel.mention}", inline=False)
            embed.add_field(name="Tiempo", value=f"<t:{int(time.time())}:R>", inline=False)
            await guild_manager.send_log_raw_message(embed=embed)

        # Salir de un canal de voz
        elif before.channel is not None and after.channel is None:
            embed = discord.Embed(title="Salida de canal de voz", color=discord.Color.red())
            embed.add_field(name="Usuario", value=f"{member.mention}", inline=False)
            embed.add_field(name="Canal", value=f"{before.channel.mention}", inline=False)
            embed.add_field(name="Tiempo", value=f"<t:{int(time.time())}:R>", inline=False)
            await guild_manager.send_log_raw_message(embed=embed)

        # Cambiar de canal de voz
        elif before.channel != after.channel:
            embed = discord.Embed(title="Cambio de canal de voz", color=discord.Color.orange())
            embed.add_field(name="Usuario", value=f"{member.mention}", inline=False)
            embed.add_field(name="De", value=f"{before.channel.mention}", inline=True)
            embed.add_field(name="A", value=f"{after.channel.mention}", inline=True)
            embed.add_field(name="Tiempo", value=f"<t:{int(time.time())}:R>", inline=False)
            await guild_manager.send_log_raw_message(embed=embed)

        # Cambiar estado de silencio o sordera
        if before.self_mute != after.self_mute or before.self_deaf != after.self_deaf:
            embed = discord.Embed(title="Cambio de estado de voz", color=discord.Color.blue())
            embed.add_field(name="Usuario", value=f"{member.mention}", inline=False)
            embed.add_field(name="Silencio", value=f"{'Sí' if after.self_mute else 'No'}", inline=True)
            embed.add_field(name="Sordera", value=f"{'Sí' if after.self_deaf else 'No'}", inline=True)
            embed.add_field(name="Tiempo", value=f"<t:{int(time.time())}:R>", inline=False)
            await guild_manager.send_log_raw_message(embed=embed)

async def setup(bot: DiscordBot):
    """
    Agrega el cog al bot
    """

    global logger
    logger = bot.logger

    await bot.add_cog(HandlerLogs(bot))