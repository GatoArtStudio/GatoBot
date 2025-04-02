from discord.ext import commands
from core.implements.guild_messenger_discord import GuildMessengerDiscord
from core.abstracts.guild_discord import GuildDiscord
from core.interfaces.handler_logs_tools import HandlerLogsTools


class GuildManagerDiscord(GuildDiscord, GuildMessengerDiscord, HandlerLogsTools):

    def __init__(self, guild_id: int, bot: commands.Bot):
        GuildDiscord.__init__(self, guild_id)
        GuildMessengerDiscord.__init__(self, guild_id, bot)
