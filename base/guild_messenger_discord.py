import discord
from discord.ext import commands
from base.guild_discord import GuildDiscord
from base.handler_logs_tools import HandlerLogsTools
import time
from typing import Optional, Sequence, Union

class GuildMessengerDiscord(HandlerLogsTools):
    def __init__(self, guild_id: int, bot: commands.Bot):
        self.guild_id = guild_id
        self.bot = bot
        self.db = GuildDiscord(guild_id)

    @HandlerLogsTools.ensure_log_channel
    async def send_log_commands_missing_permissions(self, log_channel: discord.TextChannel, interaction: discord.Interaction, error = 'Sin especificar'):

        embed = discord.Embed(title="Uso de comando sin permisos", description="Intento usar un comando sin permisos.", color=discord.Color.red())
        embed.add_field(name="Usuario", value=f"{interaction.user.display_name} ({interaction.user.id}) - <@{interaction.user.id}>", inline=False)
        embed.add_field(name="Comando", value=f"`{interaction.data['name']}`", inline=False)
        embed.add_field(name="Tiempo", value=f"<t:{int(time.time())}:R>", inline=False)
        embed.add_field(name="Error", value=f"{error}", inline=False)
        
        await log_channel.send(embed=embed, silent=True)

    @HandlerLogsTools.ensure_log_channel
    async def send_log_invite_create(self, log_channel: discord.TextChannel, invite: discord.Invite):

        embed = discord.Embed(title="Invitación creada", color=discord.Color.green())
        embed.add_field(name="Invitación", value=f"{invite.url}", inline=False)
        embed.add_field(name="Autor", value=f"{invite.inviter.mention}", inline=False)
        embed.add_field(name="Canal", value=f"{invite.channel.mention}", inline=False)
        embed.add_field(name="Tiempo", value=f"<t:{int(time.time())}:R>", inline=False)

        await log_channel.send(embed=embed, silent=True)
    
    @HandlerLogsTools.ensure_log_channel
    async def send_log_invite_delete(self, log_channel: discord.TextChannel, invite: discord.Invite, author_id: int):

        embed = discord.Embed(title="Invitación eliminada", color=discord.Color.red())
        embed.add_field(name="Invitación", value=f"{invite.url}", inline=False)
        embed.add_field(name="Autor", value=f"<@{author_id}>", inline=False)
        embed.add_field(name="Canal", value=f"{invite.channel.mention}", inline=False)
        embed.add_field(name="Tiempo", value=f"<t:{int(time.time())}:R>", inline=False)

        await log_channel.send(embed=embed, silent=True)
    
    async def send_log_raw_message(
            self,
            content: Optional[str] = None,
            *,
            tts: bool = False,
            embed: Optional[discord.Embed] = None,
            embeds: Optional[Sequence[discord.Embed]] = None,
            file: Optional[discord.File] = None,
            files: Optional[Sequence[discord.File]] = None,
            stickers: Optional[Sequence[Union[discord.GuildSticker, discord.StickerItem]]] = None,
            delete_after: Optional[float] = None,
            nonce: Optional[Union[str, int]] = None,
            allowed_mentions: Optional[discord.AllowedMentions] = None,
            reference: Optional[Union[discord.Message, discord.MessageReference, discord.PartialMessage]] = None,
            mention_author: Optional[bool] = None,
            view: Optional[discord.ui.View] = None,
            suppress_embeds: bool = False,
            silent: bool = True,
            poll: Optional[discord.Poll] = None,
            **kwargs
        ):

        log_channel_id = self.db.get_log_channel()

        if log_channel_id != 0 and log_channel_id is not None:

            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel is not None:

                await log_channel.send(
                    content=content,
                    tts=tts,
                    embed=embed,
                    embeds=embeds,
                    file=file,
                    files=files,
                    stickers=stickers,
                    delete_after=delete_after,
                    nonce=nonce,
                    allowed_mentions=allowed_mentions,
                    reference=reference,
                    mention_author=mention_author,
                    view=view,
                    suppress_embeds=suppress_embeds,
                    silent=silent,
                    poll=poll,
                    **kwargs
                )
    
    async def send_warning_raw_message(
            self,
            content: Optional[str] = None,
            *,
            tts: bool = False,
            embed: Optional[discord.Embed] = None,
            embeds: Optional[Sequence[discord.Embed]] = None,
            file: Optional[discord.File] = None,
            files: Optional[Sequence[discord.File]] = None,
            stickers: Optional[Sequence[Union[discord.GuildSticker, discord.StickerItem]]] = None,
            delete_after: Optional[float] = None,
            nonce: Optional[Union[str, int]] = None,
            allowed_mentions: Optional[discord.AllowedMentions] = None,
            reference: Optional[Union[discord.Message, discord.MessageReference, discord.PartialMessage]] = None,
            mention_author: Optional[bool] = None,
            view: Optional[discord.ui.View] = None,
            suppress_embeds: bool = False,
            silent: bool = False,
            poll: Optional[discord.Poll] = None,
            **kwargs
        ):

        warning_channel_id = self.db.get_warning_channel()

        if warning_channel_id != 0 and warning_channel_id is not None:

            channel = self.bot.get_channel(warning_channel_id)
            if channel is not None:

                await channel.send(
                    content=content,
                    tts=tts,
                    embed=embed,
                    embeds=embeds,
                    file=file,
                    files=files,
                    stickers=stickers,
                    delete_after=delete_after,
                    nonce=nonce,
                    allowed_mentions=allowed_mentions,
                    reference=reference,
                    mention_author=mention_author,
                    view=view,
                    suppress_embeds=suppress_embeds,
                    silent=silent,
                    poll=poll,
                    **kwargs
                )
    
    async def send_announcement_raw_message(
            self,
            content: Optional[str] = None,
            *,
            tts: bool = False,
            embed: Optional[discord.Embed] = None,
            embeds: Optional[Sequence[discord.Embed]] = None,
            file: Optional[discord.File] = None,
            files: Optional[Sequence[discord.File]] = None,
            stickers: Optional[Sequence[Union[discord.GuildSticker, discord.StickerItem]]] = None,
            delete_after: Optional[float] = None,
            nonce: Optional[Union[str, int]] = None,
            allowed_mentions: Optional[discord.AllowedMentions] = None,
            reference: Optional[Union[discord.Message, discord.MessageReference, discord.PartialMessage]] = None,
            mention_author: Optional[bool] = None,
            view: Optional[discord.ui.View] = None,
            suppress_embeds: bool = False,
            silent: bool = False,
            poll: Optional[discord.Poll] = None,
            **kwargs
        ):

        announcement_channel_id = self.db.get_announcement_channel()

        if announcement_channel_id != 0 and announcement_channel_id is not None:

            channel = self.bot.get_channel(announcement_channel_id)
            if channel is not None:

                await channel.send(
                    content=content,
                    tts=tts,
                    embed=embed,
                    embeds=embeds,
                    file=file,
                    files=files,
                    stickers=stickers,
                    delete_after=delete_after,
                    nonce=nonce,
                    allowed_mentions=allowed_mentions,
                    reference=reference,
                    mention_author=mention_author,
                    view=view,
                    suppress_embeds=suppress_embeds,
                    silent=silent,
                    poll=poll,
                    **kwargs
                )
    
    async def send_sanction_raw_message(
            self,
            content: Optional[str] = None,
            *,
            tts: bool = False,
            embed: Optional[discord.Embed] = None,
            embeds: Optional[Sequence[discord.Embed]] = None,
            file: Optional[discord.File] = None,
            files: Optional[Sequence[discord.File]] = None,
            stickers: Optional[Sequence[Union[discord.GuildSticker, discord.StickerItem]]] = None,
            delete_after: Optional[float] = None,
            nonce: Optional[Union[str, int]] = None,
            allowed_mentions: Optional[discord.AllowedMentions] = None,
            reference: Optional[Union[discord.Message, discord.MessageReference, discord.PartialMessage]] = None,
            mention_author: Optional[bool] = None,
            view: Optional[discord.ui.View] = None,
            suppress_embeds: bool = False,
            silent: bool = False,
            poll: Optional[discord.Poll] = None,
            **kwargs
        ):

        sanction_channel_id = self.db.get_sanction_channel()

        if sanction_channel_id != 0 and sanction_channel_id is not None:

            channel = self.bot.get_channel(sanction_channel_id)
            if channel is not None:

                await channel.send(
                    content=content,
                    tts=tts,
                    embed=embed,
                    embeds=embeds,
                    file=file,
                    files=files,
                    stickers=stickers,
                    delete_after=delete_after,
                    nonce=nonce,
                    allowed_mentions=allowed_mentions,
                    reference=reference,
                    mention_author=mention_author,
                    view=view,
                    suppress_embeds=suppress_embeds,
                    silent=silent,
                    poll=poll,
                    **kwargs
                )